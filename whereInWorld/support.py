from lib2to3.pytree import convert
import pandas as pd
import re
import geopandas
import matplotlib.pyplot as plt
import warnings

from pyparsing import lineEnd

class support:
    '''
    support class
    parses,
    writes,
    visualises
    '''
    def __init__(self):
        self.points = pd.DataFrame()
        self.gdf = geopandas.GeoDataFrame()
        self.lookup = {"N":"+","S":"-","E":"+","W":"-"}
        warnings.filterwarnings("ignore") 
        


    def parse_input(self, line:str) -> bool:
        '''
        parse input into a df
        df must be in decimal degrees

        process:
        * ID the type
        * Parse the type (or reject if DNE)
        * convert to decimal degrees 
        * create df 
        * return

        '''
        #inital cleaning
        line = line.strip("\n").strip()
        #get the words in the input
        sign = re.findall("([A-Za-z]+)", line)
        label = ""
        if (len(sign) > 0):
            if len(sign[len(sign) - 1]) > 1:
                label = sign[len(sign) - 1]

        #attempt to use decimal degrees 
        match_all = re.findall("([^0-9\s.,-]+)", line)
        split = re.findall("([-+]?[0-9.]{1,})", line)
        if (len(split) == 2 and len(sign) < 2): #i.e in decimal degrees
            self.update_df(cleaned_input=split, label=label)
            return True
        
        #new bit:
        signs = []
        for el in match_all:
            if el not in split:
                signs.append(el)
        if (len(sign) >= 8):
            sign = [signs[3], signs[7]]
            deg = [split[0], split[3]]
            min = [split[1], split[4]]
            sec = [split[2], split[5]]
            cleaned = self.convert_deg_min_sec(sign, deg, min, sec)
            self.update_df(cleaned_input=cleaned, label=label)
            return True
            

        #attempt degrees and minutes
        sign = re.findall("([A-Za-z]+)", line)
        deg = re.findall("([0-9]+)+Â°", line)
        mins = re.findall("([0-9.]+)*â€²", line)
        minsOt= re.findall("([0-9.]+)'", line)
        secs = re.findall("([0-9.]+)*â€³", line)
        secsOt= re.findall("([0-9.]+)\"", line)

        if (len(minsOt) > len(mins)):
            mins = minsOt

        if (len(secsOt) > len(secs)):
            secs = secsOt
        
        if (len(sign) > 2):
            sign = sign[0:2]

        #if these are all rational
        if (len(sign) == len(deg) == len(mins) == 2):
            if (len(secs) == 2 or len(secs) == 0):
                cleaned = self.convert_deg_min_sec(sign,deg, mins, secs)
                self.update_df(cleaned_input=cleaned, label=label)
                return True
        
        # no mins or sec
        # if at least both signs provided
        if (len(sign) == 2):
            deg = re.findall("([0-9.]+)", line)
            cleaned = self.convert_deg_min_sec(sign, deg)
            self.update_df(cleaned_input=cleaned, label=label)
            return True
        
        #mismatched/incompete format cases
        match_all = re.findall("([\w.-]+)", line)
        cleaned = [""] * 2
        ind = 0
        for el in match_all:
            if (ind > 1 or ind < 0):
                print("Unable to process")
                return True
            try:
                cleaned[ind] = (str(float(el)))
            except:
                sign = self.lookup.get(el)
                cleaned[ind-1] = sign + cleaned[ind-1]
                ind -= 1
            ind += 1
        try:
            self.update_df(cleaned_input=cleaned, label=label)
            return True
        except:
            print("Unable to process:")
            return False

    def swapTwoEl(self, list):
        '''
        swaps the position of two elemetns
        in two element list
        '''
        temp = list[0]
        list[0] = list[1]
        list[1] = temp
        return list

    def convert_deg_min_sec(self,sign,deg, mins=[0,0], secs=[0,0]) -> list:
        ''' 
        convert deg, mins, secs to 
        decimal degrees
        sign can be in wrong order!!!!
        (i.e not alwaus N , E)
        '''

        if not (sign[0] == "N" or sign[0] == "S"):
            #switch everything
            sign = self.swapTwoEl(sign)
            deg = self.swapTwoEl(deg)
            mins = self.swapTwoEl(mins)
            secs = self.swapTwoEl(secs)
            
        decDeg = [str] * 2
        deg[0] = float(deg[0])
        deg[1] = float(deg[1])
        mins[0] = float(mins[0])
        mins[1] = float(mins[1])
        if (len(secs) > 0):
            secs[0] = float(secs[0])
            secs[1] = float(secs[1])
        else:
            secs = [0,0]
        if sign[0] == "N": #positive
            decDeg[0] = "+"
        else:
            decDeg[0] = "-" 
        decDeg[0] = decDeg[0] + str(deg[0] +mins[0]/60 + secs[0]/3600)

        if sign[1] == "E": #positive
            decDeg[1] = "+"
        else:
            decDeg[1] = "-" 

        decDeg[1] = decDeg[1] + str(deg[1] + mins[1]/60 + secs[1]/3600)
        return decDeg


    def update_df(self, cleaned_input, label):
        #parse latitude        
        if (float(cleaned_input[0]) > 0):
            latitude = float(cleaned_input[0])%90.0
        else:
            latitude = float(cleaned_input[0])%-90.0
        

        #parse longitude
        if (float(cleaned_input[1]) > 0):
            longitude = float(cleaned_input[1])%180.0
        else:  
            longitude = float(cleaned_input[1])%-180.0


        df = pd.DataFrame({'Latitude': [latitude], 
                            'Longitude': [longitude],
                            'Label': [label]})
        if self.points.empty:
            self.points = df
        else:
            self.points = pd.concat([self.points,df])


    def create_gdf(self) -> geopandas.GeoDataFrame:
        '''
        creates a geodataframe
        from the current dataframe of points
        '''
        df = self.points
        self.gdf = geopandas.GeoDataFrame(
            df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude)
        )
        return self.gdf


    def makeMap(self):
        world = geopandas.read_file(geopandas.datasets.get_path(
            'naturalearth_lowres'
        ))

        ax = world.plot(color='white', edgecolor='black')

        for x, y, label in zip(self.gdf.Longitude, self.gdf.Latitude, self.gdf.Label):
            ax.annotate(label, xy=(x, y), xytext=(3,3), textcoords="offset points", color='blue')
        self.gdf.plot(ax=ax, color='red')
        plt.show()


    def write_to_file(self, fileName):
        '''
        write current gdf state to file
        '''
        self.gdf.to_file("../output/" + fileName + ".geojson", driver= "GeoJSON")
