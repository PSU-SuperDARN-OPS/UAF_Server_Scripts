#include <Python.h>
#include <datetime.h>
#include <stdio.h>
#include <zlib.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include "aacgm.h"
typedef struct {
    PyObject_HEAD
} PyAacgmObject;
/*
int AACGMLoadCoefFP(FILE  *fp);
int AACGMLoadCoef(char *fname);
int AACGMInit(int year);
int AACGMConvert(double in_lat,double in_lon,double height,
              double *out_lat,double *out_lon,double *r,
              int flag);
double AACGMConvertMLT(int yr,int yr_sec,double mlon);
*/
static PyObject *
Init(PyAacgmObject *self, PyObject *args, PyObject *kwds)
{
  int s,year=1990;
  static char *kwlist[] = {"year",NULL};
  if (! PyArg_ParseTupleAndKeywords(args, kwds, "i", kwlist,
                                      &year))
     return NULL;

  s=AACGMInit(year);
  Py_RETURN_TRUE;
}
static PyObject * Convert(PyAacgmObject *self, PyObject *args, PyObject *kwds)
{
  PyObject *list=NULL;
  double in_lat=0,in_lon=0;
  double out_lat=0,out_lon=0;
  double r=0,height=0,s=0;
  int flag=0;
  int year=-1;
  static char *kwlist[] = {"lat","lot","height","flag","year",NULL};

  if (! PyArg_ParseTupleAndKeywords(args, kwds, "ddd|ii", kwlist, 
                                      &in_lat,&in_lon,&height,&flag,&year))
     return NULL; 

  if (year > 0 ) s=AACGMInit(year);
  s=AACGMConvert(in_lat,in_lon,height,
              &out_lat,&out_lon,&r,
              flag);
  if ( s < 0 ) Py_RETURN_FALSE;
  list = PyList_New(0);
  PyList_Append(list,Py_BuildValue("d",out_lat));
  PyList_Append(list,Py_BuildValue("d",out_lon));

  return list;  

}

static PyMethodDef module_methods[] = {
   	{ "Init", (PyCFunction)Init , METH_KEYWORDS, NULL },
   	{ "Convert", (PyCFunction)Convert , METH_KEYWORDS, NULL },
	{ NULL, NULL, 0, NULL } /* Sentinel */
};
 
PyMODINIT_FUNC
initpyaacgm(void) 
{
    PyObject* m;
    m = Py_InitModule3("pyaacgm", module_methods,
                       "Module for aacgm library");

    if (m == NULL)
      return;
}
