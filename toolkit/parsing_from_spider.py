import pandas as pd
import re
from chemdataextractor.doc import Document
from chemdataextractor.reader.rsc import HtmlReader as rsc_html
from chemdataextractor.reader.acs import HtmlReader as acs_html
import spacy
from spacy.matcher import Matcher
from .logger import Logger

logger = Logger()

logger.info('spacy Load NER Model')
nlp = spacy.load("en_ner_bc5cdr_md")
logger.info('spacy Load NER Model [en_ner_bc5cdr_md] completed')

class ReaderFulltext(object):
    _ACS = 'AMER CHEMICAL SOC'
    _ELSVER = 'ELSEVIER'
    _RSC = 'ROYAL SOC CHEMISTRY'
    _ERROR_unknown_source = 'Unknown journal source!'

    
    def __init__(self, file:str,journal:str):
        self.file = file
        self.source = journal
        self.doc = self._cder_from_file()
        self.elements = self._parsing()
        self.paragraphs = self._paragraph()
        self.targeted_para = self._target_para()

    def _cder_from_file(self):

        if self.source == self._ACS:
            doc = Document.from_file(self.file,readers=[acs_html()])
        elif self.source == self._RSC:
            doc = Document.from_file(self.file,readers=[rsc_html()])
        elif self.source == self._ELSVER:
            doc = Document.from_file(self.file)
        else: raise ValueError(self._ERROR_unknown_source)
        
        logger.info(f'CDE read {self.file} from {self.source} completed.')
        return doc
    



    def _parsing(self):
        if self.source == self._ACS:
            ans = []

            for ele in self.doc.elements:
                if str(ele).startswith('Click to copy'):continue
                
                if isinstance(ele.id,str):
                    subtitle = re.search(r'^_i',ele.id)
                    sec = re.search(r'^sec',ele.id)

                    if subtitle or sec: ans.append(ele)

            if not ans:
                return None
            else:
                return [str(s).replace('\xa0',' ').replace('&nbsp;', ' ') for s in ans]
            
        elif self.source == self._RSC:

            filter_ = []
            for ele in self.doc.elements:
                if ele.id == 'pnlArticleContentLoaded': filter_.append(ele)
                if str(ele).replace('\n','') == 'Footnote': break
                if ele.id is None: filter_.append(ele)
            if not filter_: 
                return None
            else:
                return [str(s).replace('\n','').replace('\xa0',' ').replace('&nbsp;', ' ') for s in filter_] 
        
        elif self.source == self._ELSVER:

            ans =[]
            for ele in self.doc.elements:
                if ele.id is not None: 
                    ans.append(ele)
            if not ans:
                return None
            else:
                return [str(s).replace('\xa0',' ').replace('&nbsp;', ' ') for s in ans]

        else:
            raise  ValueError(self._ERROR_unknown_source)
        
        



    def _paragraph(self):

        file_name = self.file.split('/')[-1]
        if self.source == self._ACS:
            ans = []

            for ele in self.doc.elements:
                if str(ele).startswith('Click to copy'):continue
                
                if isinstance(ele.id,str):
                    sec = re.search(r'^sec',ele.id)

                    if sec: ans.append(ele)
            
            logger.info(f'Found {len(ans)} paragraphes in {file_name} from {self.source}')
            if not ans:
                return None
            else:
                return [str(s).replace('\xa0',' ').replace('&nbsp;', ' ') for s in ans]
            
        elif self.source == self._RSC:

            filter_ = []
            for ele in self.doc.elements:
                if ele.id == 'pnlArticleContentLoaded': filter_.append(ele)
                if str(ele).replace('\n','') == 'Footnote': break
            logger.info(f'Found {len(filter_)} paragraphes in {file_name} from {self.source}')
            if not filter_: 
                return None
            else:
                return [str(s).replace('\n','').replace('\xa0',' ').replace('&nbsp;', ' ') for s in filter_]
        
        elif self.source == self._ELSVER:

            ans =[]
            for ele in self.doc.elements:
                if isinstance(ele.id,str):
                    is_para = re.search(r'^p\d\d|^para',ele.id,re.I)
                    if is_para: 
                        ans.append(ele)
            logger.info(f'Found {len(ans)} paragraphes in {file_name} from {self.source}')
            if not ans:
                return None
            else:
                return [str(s).replace('\xa0',' ').replace('&nbsp;', ' ') for s in ans]

        else:
            raise  ValueError(self._ERROR_unknown_source)

    def _judge_paragraphe(self,para):

        matcher = Matcher(nlp.vocab)

        patterns = [
            
            [{"TEXT": {"REGEX": r"(?i)^(D[159]0|PDI|d\d{2})$"}}],
            
            [{"LOWER": {"IN": ["mean", "average", "median"]}}, 
            {"LOWER": {"IN": ["particle", "crystal", "droplet"]}, "OP": "?"}, 
            {"LOWER": {"IN": ["size", "diameter"]}}],
            
            [{"TAG": "CD"}, {"LOWER": {"IN": ["nm", "μm", "um", "microns", "nanometers"]}}]
        ]
        matcher.add("PARTICLE_SIZE_DATA", patterns)

        doc = nlp(para)
        matches = matcher(doc)
        
        has_statistical_metric = any(doc[start:end].text.lower() in ['d50', 'pdi', 'd10', 'd90'] for _, start, end in matches)
        
        if len(matches) >= 2 or has_statistical_metric:
            return True
        

        chemicals = [ent for ent in doc.ents if ent.label_ == "CHEMICAL"]
        if len(chemicals) < 2:
            return False
        
        measurements = 0
        liquid_units = {'ml', 'l', 'ul', 'microliter'}
        mass_units = {'mg', 'g', 'mmol', 'mol','M','mM','nM', '℃'}
        time_units = {'s','min','minutes','h','hours'}
        for i in range(len(doc) - 1):
            if doc[i].tag_ == "CD": 
                next_token = doc[i+1].text.lower()
                if next_token in liquid_units or next_token in mass_units or next_token in time_units:
                    measurements += 1

        return len(chemicals) >= 2 and  measurements >= 2

        

    def _target_para(self):
        
        file_name = self.file.split('/')[-1]
        target_para = []
        if self.paragraphs is None:
            return None
        for para in self.paragraphs:
            if self._judge_paragraphe(para):
                target_para.append(para)
        logger.info(f'Found {len(target_para)} target paragraphes in {file_name} from {self.source}')
        if target_para:
            return target_para
        else: return None


