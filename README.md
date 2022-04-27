# jBeam

![image](https://user-images.githubusercontent.com/43247197/165540716-4a783589-1d23-4045-a668-2e64cad28680.png)

THIS PROJECT IS VERY MUCH A WIP

#### Step 1 - Clone and Install Dependencies:
`git clone https://github.com/connorivy/jBeam.git`

** Optional - create virtual environment `py -3.9 -m venv venv` `venv\Scripts\activate.bat` **

`pip install -r requirements.txt`

Another depencency that is needed is my fork of [SymBeam](https://github.com/connorivy/symbeam).
In the project folder, run `git clone https://github.com/connorivy/symbeam.git` and then cd to that folder and run `pip install .`

#### Step 2 - Run Local Server:

`python manage.py runserver`

#### Step 3 - Adjust Beam Length:
![beam_len](https://user-images.githubusercontent.com/43247197/165534826-df4f4191-956f-4f21-89ae-407934aba5b5.gif)

#### Step 3 - Add and Edit Loads:
![adjust_loads](https://user-images.githubusercontent.com/43247197/165538640-82b14453-4eb8-4f72-807c-b5b82ac3dacf.gif)

#### Step 4 - Run Analysis:
![analysis](https://user-images.githubusercontent.com/43247197/165539721-e60104ed-bbf3-41ee-b140-0b8c2366b115.gif)

Run the analysis by pressing the calculator icon. This calculates and renders the shear, moment, and deflection diagram for the beam. A beam size will also be populated. At the moment, this beam size comes from a VERY limited selection of wide flange sizes, and it selects the smallest shape that satisfies the L/240 total deflection criteria. There are no checks for any sort of beam failure. **DO NOT USE TO DESIGN REAL-WOLRD BEAMS**

Next items to be implemented:
- [ ] Fixing bugs with adding and deleting loads
- [ ] Making the UI look better
- [ ] Strength calculation for steel beams
- [ ] Report that shows all calculations
- [ ] 'Distance between adjacent beams' functionality to enable composite beam calculations
- [ ] Make units more apparent and allow user to change units
- [ ] Add unittests for strength and deflection calculations
