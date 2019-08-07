#!/usr/bin/env python

__author__ = "Maros Kukan"
__author_email__ = "maros.kukan@me.com"
__license__ = "GPL"

import argparse, json, yaml, xml, xmltodict


def convert(infile, informat, outformat, verbose):
    """
    Read source file, convert if dictionary and based on selection
    convert it to desired data format. Optionally display the content
    of result file.
    """
    try:
        with open(infile) as f:
            # Convert the input data to dictionary
            if informat == "json":
                pydict = json.load(f)
            elif informat == "yaml":
                pydict = yaml.safe_load(f)
            elif informat == "xml":
                pydict = xmltodict.parse(f.read())
            else:
                print("Unknown input format.")
                return None
    except ValueError as e:
        print('Error: Invalid file format: {} {}'.format(infile, e))
        return None
    except xml.parsers.expat.ExpatError as e:
        print('Error: Invalid xml file: {} {}'.format(infile, e))
        return None
    except FileNotFoundError as e:
        print('Error: File not found: {} {}'.format(infile, e))
        return None
    

    outname = infile.split(".")[0]

    if outformat == "json":
        data = json.dumps(pydict)
    elif outformat == "yaml":
        data = yaml.dump(pydict)
    elif outformat == "xml":
        data = xmltodict.unparse(pydict) 
    else:
        print("Unknown output format.")
        return None
    
    # Write output file
    with open("{}_out.{}".format(outname, outformat), "w") as f:
        f.write(data)
    print("Sucess: Data saved to {}_out.{}\n".format(outname, outformat))

    # Optionally prit the file content on the screen
    if verbose:
        print("File content:\n")
        with open("{}.{}".format(outname, outformat), "r") as f:
            print(f.read())
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    # Mndatory arguments
    parser.add_argument('--file', required=True, help='source file name')
    parser.add_argument('--informat', required=True, help='source file format (json, xml, yaml)')
    parser.add_argument('--outformat', required=True, help='output file format (json,xml yaml')
    
    # Optional arguments
    parser.add_argument('--verbose', action='store_true', help='display output file content')
    
    args = parser.parse_args()

    convert(infile=args.file,
            informat=args.informat,
            outformat=args.outformat,
            verbose=args.verbose)
    

    
    
