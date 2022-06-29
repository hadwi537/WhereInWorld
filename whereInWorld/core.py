import sys
from support import support
from datetime import date

if __name__ == "__main__":
    '''
    entry point
    '''
    parser = support()
    for line in sys.stdin:
        if 'Exit' == line.rstrip():
            break
        if(parser.parse_input(line)):
            print(f'line input: {line}\n')
        

    parser.create_gdf() #create the geodataframe
    parser.makeMap() #create and draw the map
    parser.write_to_file(str(date.today())) #write  gdf to file