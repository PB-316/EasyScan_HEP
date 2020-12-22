#!/usr/bin/env python
####################################################################
#    Some usefull functions
####################################################################

# External modules.
import time, os, sys
from collections import OrderedDict
# Internal modules
from initialize import logger

## Define 'negetive infinity'
log_zero = -1e+100
## Define 'not a number'
NaN = float('NaN')
## Define current path
CurrentPath = os.getcwd()

## Define screen print functions
def ColorText(i,text,j=1):
    return '\033[%i;3%i;2m %s\033[0m' %(j,i,text)
def GotoWeb():
    print(ColorText(1,'# Goto ') + ColorText(1,'https://github.com/phyzhangyang/EasyScan_HEP',4) + ColorText(1,' for detail.'))
def WarningWait(warinfo):
    logger.warning(ColorText(1,warinfo))
    print(ColorText(1,'# Waiting 3 seconds for WARNING.'))
    time.sleep(3)
def WarningNoWait(warinfo):
    logger.warning(ColorText(1,warinfo))
def ErrorStop(errinfo):
    logger.error( ColorText(1,errinfo) )
    GotoWeb()
    print(ColorText(1,'# Exiting with ERROR.'))
    sys.exit(1)
def Info(debinfo):
    logger.info( ColorText(2,debinfo) )
def Debug(debinfo,debvalue=''):
    if debvalue=='':
        logger.debug( ColorText(5, str(debinfo) ) )
    else:
        logger.debug( ColorText(5, str(debinfo)+': '+str(debvalue) ) )

## Transform str into int and float
def autotype(s):
    if type(s) is not str:
        return s
    if s.isdigit():
        return int(s)
    try:
        return float(s)
    except ValueError:
        return s

## Transform str into list
def string2list(s):
    s = [ autotype(ss.strip()) for ss in s.split('\n') ]
    return s

## Parse string of input variable and output variable in configure file to list of items.
def string2nestlist(s):
    s = [x.split(',') for x in s.split('\n')]
    s = [[autotype(x.strip()) for x in ss] for ss in s]
    return s

## Write information of result into file
# TODO why 'postprocess' is return
def WriteResultInf(InPar,OutPar,Constraint,Path,ScanMethod,File):
    if ScanMethod == 'PLOT': return
    #if ScanMethod == 'POSTPROCESS': os.rename(os.path.join(Path,'ScanInf.txt'),os.path.join(Path,'ScanInf_old.txt'))
    file_inf = open(os.path.join(Path,'ScanInf.txt'),'w')
    file_inf.write('\t'.join([Path, File])+'\n') # TODO is there any possibility that we do not need this?
    icount = 0
    if ScanMethod == 'MULTINEST':
        file_inf.write('probability\t0\n')
        file_inf.write('-2*loglikehood\t1\n')
        icount += 2
    for name in InPar:
        file_inf.write('\t'.join([name,str(icount)])+'\n')
        icount += 1
    for name in OutPar :
        file_inf.write('\t'.join([name,str(icount)])+'\n')
        icount += 1
    ## new 20180428 liang
    for name in Constraint:
        file_inf.write('\t'.join([name,str(icount)])+'\n')
        icount += 1
    if ScanMethod == 'MCMC':
        file_inf.write('\t'.join(['mult',str(icount)])+'\n')
    file_inf.close()

## Evaluate a math string
# http://lybniz2.sourceforge.net/safeeval.html
# Make a list of safe functions
safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh',
             'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 
             'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 
             'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
# Use the list to filter the local namespace
safe_dict = dict([ (k, globals().get(k, None)) for k in safe_list ])
# Add any needed builtins back in.
safe_dict['abs'] = abs
safe_dict['float'] = float 
safe_dict['int'] = int 
def parseMath(par):
    safe_dict.update(par)
    safe_dict.update({"__builtins__": None})
    for key,value in par.items():
        expr = ','.join(key.split(';'))
        try:
            cal = eval(expr, safe_dict)
        except SyntaxError:
            for keyAlt,valueAlt in par.items():
                if type(valueAlt) == str:
                    expr=expr.replace(keyAlt, valueAlt)
                else:
                    if isnan(valueAlt): 
                        expr=expr.replace(keyAlt, "float('NaN')")
                    else:
                        expr=expr.replace(keyAlt, str(valueAlt))
            cal = eval(expr, safe_dict)

        #print key, expr, cal; raw_input("math") 
        par[key] = cal
        
## Delete path in the name of files
# TODO don't save file name
def checkFileInList(List):
    newList=[]
    files=[]
    for item in List:
        try:
            float(item)
            newList.append(item)
        except ValueError:
            if item.find('/') >= 0:
                files.append(item)
                newList.append(item.split('/')[-1])
            else:
                newList.append(item)

    return newList, files

# Sort parameters so that we can output them in right order
def sortDic(Dic):
    return OrderedDict(sorted(list(Dic.items()), key = lambda t: t[0]))
       
