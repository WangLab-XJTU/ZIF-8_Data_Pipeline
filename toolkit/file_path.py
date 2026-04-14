import os
import pandas as pd
from .logger import Logger
import hashlib
logger = Logger()

class FilePath(object):
    

    def __init__(self, **kwargs):

        self.fulltext_path = kwargs.get('fulltext_path', 'Spider/Fulltext')
        self.filemapping = kwargs.get('filemapping', 'Spider/File_name.csv')
        self.index_file = kwargs.get('index_file', 'Filter_1.xlsx')
        self.save_data = kwargs.get('save_path', 'out.xlsx')
        self.matedata = kwargs.get('matedata', 'matedata.xlsx')
        self.done_file = kwargs.get('done_file','Verify')
        self.not_match_count = 0
        
    def get_next_task(self): 

        df = pd.read_excel(self.matedata)
        tasks = df[df['Task']]
        count_task = len(tasks)
        if count_task != 0:
            logger.info(f'{count_task} Task Found')
        else:
            
            logger.info(f'Task all completed')
            return None,None,None
        task = tasks.sample(n=1)[['DOI','Publisher','Fulltext']].iloc[0].to_list()
        task[2] = os.path.join(self.fulltext_path, task[2])
        logger.info(f'Submit extraction task DOI: {task[0]}, Publisher: {task[1]}.')
        return tuple(task)

    def save_extract_data(self,doi,extract_data):

        if not os.path.exists(self.save_data):
            logger.info(f'Initialization out file {self.save_data}')
            return self._init_outfile(doi,extract_data)
        
        extract_data = pd.DataFrame(extract_data)
        out = pd.read_excel(self.save_data)
        extract_data['DOI'] = doi
        out_keys = out.columns.to_list()
        extract_data_keys = extract_data.columns.to_list()
        if out_keys == extract_data_keys:
            out = pd.concat([out,extract_data],ignore_index=True,axis=0)
            out.to_excel(self.save_data,index=False)
            logger.info(f'Task {doi} extract data saved {self.save_data}')

            self._updata_matedata(doi)
        else:
            self.not_match_count += 1
            logger.error(f'In {doi} task, keys not match! Counter: {self.not_match_count}')
    

    def _init_outfile(self,doi,extract_data):

        extract_data = pd.DataFrame(extract_data)
        extract_data['DOI'] = doi
        extract_data.to_excel(self.save_data,index=False)
        logger.info(f'Out file {self.save_data} created.')

        self._updata_matedata(doi)

    def _updata_matedata(self,doi):
        
        matedata = pd.read_excel(self.matedata)
        matedata.loc[matedata['DOI']==doi,'Task'] = False
        matedata.to_excel(self.matedata,index=False)
        logger.info(f'Updata matedata from {doi}')



    def verify_file_writer(self,doi,text=False,file_name=False):
        if not os.path.exists(self.done_file):
            os.mkdir(self.done_file)
            logger.info(f'Initialization Verify file created')


        file_path = os.path.join(self.done_file,hashlib.md5(doi.encode()).hexdigest())
        
        if not os.path.exists(file_path):
            os.mkdir(file_path)
            matedata = pd.read_excel(self.matedata)
            matedata.loc[matedata['DOI']==doi].to_csv(os.path.join(file_path,'matedata'))
            logger.info(f'Initialization Verify file from {doi} created.')

        if text and file_name:
            with open(os.path.join(file_path,file_name),'w') as f:
                f.write(text)

            logger.info(f'Verify file from {doi}, write {file_name}')




    def make_matedata(self):
        
        df = pd.read_excel(self.index_file)
        index_ = df.loc[:,['DOI','Publisher','Article Title']]
        file_mapping = pd.read_csv(self.filemapping,header=None)
        file_mapping.columns = ['key','value']
        file_mapping.index = file_mapping['key']
        mapping = file_mapping['value'].to_dict()

        index_ = index_.assign(Fulltext = lambda d:d['DOI'].map(mapping))
        if index_['Fulltext'].isna().any():
            count = index_['Fulltext'].isna().sum()
            logger.info(f'Found Fulltext has NA,{count} items were not found')
        index_['Task'] = True
        index_[~index_.isna().any(axis=1)].to_excel(self.matedata,index=False)
    
        logger.info(f'Maked matedata {self.matedata},File created.')

if __name__ == '__main__':
    File_ = FilePath()
    #File_.make_matedata()
    print(File_.get_next_task())






