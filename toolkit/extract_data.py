import os
from openai import OpenAI
from dotenv import load_dotenv
from .logger import Logger
import json

SYSTEM_PROMPT = '''### ### Role
You are an expert Data Analyst specializing in Metal-Organic Frameworks (MOFs) and materials science literature. 

### Task
Carefully read the provided experimental procedures and extract the synthesis parameters for ALL mentioned samples. 

### Extraction & Standardization Rules
1. **Array of Objects:** Output a single JSON array `[...]` containing flat JSON objects. Do NOT use nested JSON structures. 
2. **Value and Unit Separation:** Separate physical quantities into `_value` (pure float/integer) and `_unit` (string). 
3. **Missing Values:** If a parameter is not explicitly mentioned, output `null` for both value and unit. Do not guess.
4. **Terminology Standardization (Crucial):**
   - **Solvents:** Unify synonymous terms. For example, always output "water" for "deionized water", "DI water", or "Milli-Q water". For mixtures, use the format "solvent A/solvent B" (e.g., "methanol/water").
   - **Ligands:** Use standard chemical abbreviations if widely recognized (e.g., use "2-MeIM" instead of "2-methylimidazole").
   - **Sample Types:** Strictly use one of the following categories: "Target Product", "Intermediate", "Control Group", or "Sacrificial Template".
   - **Methods:** Standardize basic actions (e.g., use "stirring", "sonication", "static", "hydrothermal", "vapor-phase deposition").

### Output Format (JSON Array)
[
  {
    "sample_name": "string // Specific name of the sample from the text (e.g., 'ZIF-8-HS', 'ZIF-8 film')",
    "sample_type": "string // Must be: 'Target Product', 'Intermediate', 'Control Group', or 'Sacrificial Template'",
    
    "synthesis_method": "string // e.g., 'hydrothermal', 'room-temperature aqueous', 'epitaxial growth', 'vapor-phase deposition'",
    
    "metal_source_name": "string // Chemical formula preferred (e.g., 'Zn(NO3)2·6H2O', 'ZnO')",
    "metal_source_amount_value": float,
    "metal_source_amount_unit": "string",
    "metal_source_concentration_value": float,
    "metal_source_concentration_unit": "string",
    
    "ligand_name": "string // Standard abbreviation (e.g., '2-MeIM')",
    "ligand_amount_value": float,
    "ligand_amount_unit": "string",
    "ligand_concentration_value": float,
    "ligand_concentration_unit": "string",
    
    "additive_or_template_name": "string // Any surfactant, modulator, or template (e.g., 'CTAB', 'PVP', 'ZIF-67')",Please record all. If there are more than one, please give a list, and the order is corresponding
    "additive_amount_value": float,
    "additive_amount_unit": "string",
    
    "solvent_name": "string // Standardized name (e.g., 'water', 'methanol', 'N,N-dimethylformamide')",
    "solvent_volume_value": float,
    "solvent_volume_unit": "string",
    
    "stirring_method": "string // e.g., 'stirring', 'sonication', 'static'",
    "temperature_value": float,
    "temperature_unit": "string",
    "reaction_time_value": float,
    "reaction_time_unit": "string",
    
    "morphology": "string // Standardized descriptors (e.g., 'nanosphere', 'thin film', 'hollow sphere', 'nanocube')",
    "size_value": float // If it's a film/shell, input the thickness here.,
    "size_unit": "string"
  }
]

### User Input
[Insert your experimental data or literature abstract here]'''

logger = Logger()

class Extractor:
    def __init__(self, api_key=None, base_url="https://api.deepseek.com"):

        load_dotenv()
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        
        if not self.api_key:
            raise ValueError("API key not found! Please set the environment variable or pass it in during initialization.")

       
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)
        logger.info(f'Initialization LLM API client Done')
            
    def extract_data(self, text, system_prompt= SYSTEM_PROMPT, model="deepseek-chat", stream=False, temperature=0,**kwargs):
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]

        try:

            logger.info(f'Create a request, Waiting for API response....')
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream,
                temperature = temperature,
                response_format={"type": "json_object"},
                **kwargs
            )
            
            if stream:
                return response  
            logger.info(f'API Request completed!')

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error requesting Extractor: {e}")
            return None

if __name__ == "__main__":
    extractor = Extractor()
    
    text = '''To confirm the successful synthesis of ZIF-8 and analyze its morphological structures, transmission electron microscopy (TEM) is used to collect high-resolution images. These images are further analyzed using ImageJ software to characterize the sizes of individual ZIF-8 nanoparticles. Based on the imaging results, a total of 100 nanoparticles are identified and analyzed for each synthesis condition, which provides the data to determine the size distribution and estimate the average size. The average size per synthesis is saved and used for the development of ML models.'''
    text = "Typically, 293 mg of Zn(OAc)2 was first dissolved in 10 mL of DI water and then the solution added to another solution consisting of 1.08 g of Hmim in 20 mL of DI water without stirring at room temperature (∼25 ± 2 °C). The final molar composition of the synthesis solution was Zn/Hmim/water = 1/35/1280. After aging for 24 h, the precipitate was separated from the colloidal dispersion by centrifugation (7000 rpm, 5 min) and washed with DI water three times. To examine the effects of the molar ratio of Hmim/Zn on the as-synthesized products, the Hmim/Zn molar ratio was adjusted from 10 to 70 by adjusting the concentration of Hmim at a fixed Zn concentration (0.78 mmol L−1). Finally, the obtained products were then dried in air for 24 h at 60 °C for subsequent characterization. Syntheses of ZIF-8 using other zinc sources, e.g. ZnSO4, Zn(NO3)2, ZnCl2, ZnBr2, ZnI2, followed similar procedures.\nXRD patterns were recorded on a diffractometer (AXS, Brucker, Germany) with Cu target (40 kV, 40 mA, λ = 1.54059 Å) from 3° to 55° at a scan rate of 2° min−1 with a step size of 0.02°. The surface morphologies and elemental compositions of products were examined by SEM (SU-8020, Hitachi, Japan) coupled with Energy-dispersive X-ray spectroscopy (EDX) (INCA-X, Oxford, Japan) operated at an acceleration voltage of 1–15 kV in a high vacuum mode. Samples were mounted using a conductive carbon double-sided sticky tape. A thin (ca. 10 nm) coating of gold was sputtered onto the samples to reduce the effects of charging. The diameters of more than 200 particles in the SEM images were measured to determine the average particle size (d) and coefficient of variation (R2) defined by Gaussian fitting equation. The nitrogen adsorption isotherms were measured at liquid nitrogen temperature (77 K) using a gas adsorption analyzer (ASAP2020HD88; Micromeritics, USA), the sample was degassed at 150 °C for 3 h under vacuum prior to measure. The surface area was then calculated using the Brunauer–Emmett–Teller (BET) method based on adsorption data. pH values of solution were measured by a pH meter (Orion 3Star, Thermo, USA). The functional groups of products were identified by Fourier transform infrared spectroscopy (FT-IR) (Tenson 27; Bruker, Germany) in transmission mode.\nFurthermore, the size statistics of ZIF-8 particles prepared from different zinc salts were measured. As shown in Fig. 2, the sizes of the resulting particles decreased with an increase of the amount of Hmim. For example, the average size of particles prepared from ZnSO4 decreases to 231 nm from 1.64 μm as Hmim/Zn ratio increases to 70 from 35. ZIF-8 particles prepared from Zn(OAc)2 have a narrow size distribution with average particle size of around 746 nm at the Hmim/Zn = 70. The sizes of particles using ZnCl2 and Zn(NO3)2 as zinc source are also smaller. The ZIF-8 synthesized using ZnBr2 at the Hmim/Zn molar ratio of 70 has the narrowest size distribution with the mean size of only 26.4 nm. This result indicates that the crystal size of ZIF-8 depends on both Hmim concentration and zinc source.\nFig. 6 shows effect of the water amount in the synthesis of ZIF-8 crystals on XRD patterns at the constant Hmim/Zn molar ratio of 10. When the water content decreased from the Zn/Hmim/H2O molar ratio of 1/10/2476 to 1/10/1238, the products exhibit the same diffraction peaks with unidentified XRD phases, which can be indexed to some by-products. However, with decreasing water amount to Zn/Hmim/H2O molar ratio of 1/10/805, the intensity of reflection peaks of the by-products decreased and the notable peak of dia(Zn) for ZIF-8, corresponding to the {011} plane, appears. Moreover, the intensity of {011} peak increases as the amount of water decreases further (Fig. 6). Similar result was also found by the previous report.25 On the other hand, we noticed that high concentration of precursor solution triggered a rapid coordination reaction. The solution prepared at the Zn/Hmim/H2O molar ratio of 1/10/310 turns completely cloudy within 90 s, although precipitates appeared in all solutions after aging 24 h (Fig. 6 inserted). It is worth noting that we found zinc concentration has less effect on the color change in solution (data not shown). This observation indicates that the high Hmim concentration may significantly accelerate the nucleation process of ZIF-8 crystals.\nFig. 11 compares the change of XRD of the synthesized ZIF-8 with the synthesis time. Clearly, at the very initial period within only 5 minutes from Zn(OAc)2, the typical XRD patterns of ZIF-8 can be readily obtained despite relatively weak peak of dia(Zn) for ZIF-8 at 2θ = 7°. However, the prominent peak, corresponding to the {011} plane of SOD-type ZIF-8 crystal, increases with reaction time. Furthermore, we quantified the {011} peak area under the Gaussian fitting curve after baseline correction, to determine the relative crystallinity level of ZIF-8 particles at different phases (Table 1) according to Venna's method.34 The relative crystallinity of ZIF-8 particles was in a low degree (about 15–20%), but a rapid increase was shown at 8 h. Next, the value increased to 97% at 16 h and stayed practically unchanged until reaching a maximum of 100% at 3 days."
    response = extractor.extract_data(text)
    print(response)
