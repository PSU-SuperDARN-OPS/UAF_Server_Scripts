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
#include "limits.h"
#include "radar.h"
#include "rpos.h"
#include "calcvector.h"
typedef struct {
    PyObject_HEAD
} PyRPosObject;


static PyObject *
CalcVector(PyRPosObject *self, PyObject *args, PyObject *kwds)
{
  PyObject *location=NULL,*list=NULL, *timetuple=NULL;
  double lat=0,lon=0,mag, azm;
  double clat, clon;
  char *radarcode;
  int stid;
  struct RadarNetwork *network;
  struct Radar *radar;
  struct RadarSite *site;
  static char *kwlist[] = {"mag","azm","location","radarcode","radarid",NULL};
  char *envstr=NULL;
  FILE *fp;
  int yr,mo,dy,hr,mt;
  double sc;
  yr=2008;
  mo=7;
  dy=12;
  hr=12;
  mt=0;
  sc=0; 

  radarcode="kod";
  stid=-1;

  if (! PyArg_ParseTupleAndKeywords(args, kwds, "dd|Osi", kwlist, 
                                      &mag,&azm,&location,&radarcode,&stid))
     return NULL; 

  if ( timetuple != NULL) {
    if (PyDateTime_Check(timetuple)) {	
      yr=PyDateTime_GET_YEAR(timetuple);   
      mo=PyDateTime_GET_MONTH(timetuple);  
      dy=PyDateTime_GET_DAY(timetuple);   
      hr=PyDateTime_DATE_GET_HOUR(timetuple);   
      mt=PyDateTime_DATE_GET_MINUTE(timetuple);   
      sc=PyDateTime_DATE_GET_SECOND(timetuple);   
    }
  } 

  if ( location != NULL) {
    if (PyTuple_Check(location) && PyTuple_Size(location)==2) {	
      lat=PyFloat_AS_DOUBLE(PyTuple_GetItem(location,0));
      lon=PyFloat_AS_DOUBLE(PyTuple_GetItem(location,1));
    }
  } else {
    envstr=getenv("SD_RADAR");
    if (envstr==NULL) {
      fprintf(stderr,"Environment variable 'SD_RADAR' must be defined.\n");
      exit(-1);
    }

    fp=fopen(envstr,"r");

    if (fp==NULL) {
      fprintf(stderr,"Could not locate radar information file.\n");
      exit(-1);
    }

    network=RadarLoad(fp);
    fclose(fp); 

    if (network==NULL) {
      fprintf(stderr,"Failed to read radar information.\n");
      exit(-1);
    }

    envstr=getenv("SD_HDWPATH");
    if (envstr==NULL) {
      fprintf(stderr,"Environment variable 'SD_HDWPATH' must be defined.\n");
      exit(-1);
    }

    RadarLoadHardware(envstr,network);

    if (stid==-1) {
      stid=RadarGetID(network,radarcode);
    } 
    radar=RadarGetRadar(network,stid);
    site=RadarYMDHMSGetSite(radar,yr,mo,dy,hr,mt,(int) sc);
    lat=site->geolat;
    lon=site->geolon;
  }
  RPosCalcVector(lat,lon,mag,azm,&clat,&clon);
  list = PyList_New(0);
  PyList_Append(list,Py_BuildValue("d",clat));
  PyList_Append(list,Py_BuildValue("d",clon));

  return list;  

}

static PyObject *
PosCubic(PyRPosObject *self, PyObject *args, PyObject *kwds)
{
  PyObject *list=NULL, *timetuple=NULL;
  char *radarcode;
  struct RadarNetwork *network;
  struct Radar *radar;
  struct RadarSite *site;
  int center, bcrd, rcrd;
  int frang,rsep,rxrise,height;
  int yr,mo,dy,hr,mt;
  double sc;
  int stid;
  double x,y,z;
  char *envstr=NULL;
  FILE *fp;

  static char *kwlist[] = {"center","bcrd","rcrd","frang","rsep","rxrise","height", "radarcode","radarid","time",NULL};
  PyDateTime_IMPORT;
  center=0;
  bcrd=1;
  rcrd=15;
  frang=1200;
  rxrise=0;
  rsep=100;
  height=300;
  radarcode="kod";
  stid=-1;
  yr=2008;
  mo=7;
  dy=12;
  hr=12;
  mt=0;
  sc=0; 

  if (! PyArg_ParseTupleAndKeywords(args, kwds, "|iiiiiiisiO", kwlist, 
                                      &center,&bcrd,&rcrd,&frang,&rsep,&rxrise,&height,&radarcode,&stid,&timetuple))
     return NULL; 

  if ( timetuple != NULL) {
    if (PyDateTime_Check(timetuple)) {	
      yr=PyDateTime_GET_YEAR(timetuple);   
      mo=PyDateTime_GET_MONTH(timetuple);  
      dy=PyDateTime_GET_DAY(timetuple);   
      hr=PyDateTime_DATE_GET_HOUR(timetuple);   
      mt=PyDateTime_DATE_GET_MINUTE(timetuple);   
      sc=PyDateTime_DATE_GET_SECOND(timetuple);   
    }
  }
  envstr=getenv("SD_RADAR");
  if (envstr==NULL) {
    fprintf(stderr,"Environment variable 'SD_RADAR' must be defined.\n");
    exit(-1);
  }

  fp=fopen(envstr,"r");

  if (fp==NULL) {
    fprintf(stderr,"Could not locate radar information file.\n");
    exit(-1);
  }

  network=RadarLoad(fp);
  fclose(fp); 

  if (network==NULL) {
    fprintf(stderr,"Failed to read radar information.\n");
    exit(-1);
  }

  envstr=getenv("SD_HDWPATH");
  if (envstr==NULL) {
    fprintf(stderr,"Environment variable 'SD_HDWPATH' must be defined.\n");
    exit(-1);
  }

  RadarLoadHardware(envstr,network);


  if (stid==-1) {
    stid=RadarGetID(network,radarcode);
  }
  radar=RadarGetRadar(network,stid);
  site=RadarYMDHMSGetSite(radar,yr,mo,dy,hr,mt,(int) sc);
  RPosCubicGS(center,bcrd,rcrd,site,frang,rsep,rxrise,height,&x,&y,&z);
  list = PyList_New(0);
  PyList_Append(list,Py_BuildValue("d",x));
  PyList_Append(list,Py_BuildValue("d",y));
  PyList_Append(list,Py_BuildValue("d",z));

  return list;  
}



static PyObject *
PosGeo(PyRPosObject *self, PyObject *args, PyObject *kwds)
{
  PyObject *list=NULL, *timetuple=NULL;
  char *radarcode;
  struct RadarNetwork *network;
  struct Radar *radar;
  struct RadarSite *site;
  int center, bcrd, rcrd;
  int frang,rsep,rxrise,height;
  int yr,mo,dy,hr,mt;
  double sc;
  int stid;
  double rho,lat,lng;
  char *envstr=NULL;
  FILE *fp;
  int r,c;
  static char *kwlist[] = {"center","bcrd","rcrd","frang","rsep","rxrise","height", "radarcode","radarid","time",NULL};
  PyDateTime_IMPORT;
  center=0;
  bcrd=1;
  rcrd=15;
  frang=1200;
  rxrise=0;
  rsep=100;
  height=300;
  radarcode="kod";
  stid=-1;
  yr=2008;
  mo=7;
  dy=12;
  hr=12;
  mt=0;
  sc=0; 

  if (! PyArg_ParseTupleAndKeywords(args, kwds, "|iiiiiiisiO", kwlist, 
                                      &center,&bcrd,&rcrd,&frang,&rsep,&rxrise,&height,&radarcode,&stid,&timetuple))
     return NULL; 

  if ( timetuple != NULL) {
    if (PyDateTime_Check(timetuple)) {	
      yr=PyDateTime_GET_YEAR(timetuple);   
      mo=PyDateTime_GET_MONTH(timetuple);  
      dy=PyDateTime_GET_DAY(timetuple);   
      hr=PyDateTime_DATE_GET_HOUR(timetuple);   
      mt=PyDateTime_DATE_GET_MINUTE(timetuple);   
      sc=PyDateTime_DATE_GET_SECOND(timetuple);   
    }
  }
  envstr=getenv("SD_RADAR");
  if (envstr==NULL) {
    fprintf(stderr,"Environment variable 'SD_RADAR' must be defined.\n");
    exit(-1);
  }

  fp=fopen(envstr,"r");

  if (fp==NULL) {
    fprintf(stderr,"Could not locate radar information file.\n");
    exit(-1);
  }

  network=RadarLoad(fp);
  fclose(fp); 

  if (network==NULL) {
    fprintf(stderr,"Failed to read radar information.\n");
    exit(-1);
  }

  envstr=getenv("SD_HDWPATH");
  if (envstr==NULL) {
    fprintf(stderr,"Environment variable 'SD_HDWPATH' must be defined.\n");
    exit(-1);
  }

  RadarLoadHardware(envstr,network);


  if (stid==-1) {
    stid=RadarGetID(network,radarcode);
  }
  radar=RadarGetRadar(network,stid);
  site=RadarYMDHMSGetSite(radar,yr,mo,dy,hr,mt,(int) sc);
  RPosGeo(center,bcrd,rcrd,site,frang,rsep,rxrise,height,&rho,&lat,&lng);
  radar=NULL;
  site=NULL;
  for (r=0;r<network->rnum;r++) {
    for (c=0;c<network->radar[r].cnum;c++) { 
      if (network->radar[r].code[c] !=NULL) free(network->radar[r].code[c]);
    } 
    if (network->radar[r].code !=NULL) free(network->radar[r].code);
    if (network->radar[r].name !=NULL) free(network->radar[r].name);
    if (network->radar[r].operator !=NULL) free(network->radar[r].operator);
    if (network->radar[r].hdwfname !=NULL) free(network->radar[r].hdwfname);
    if (network->radar[r].site !=NULL) free(network->radar[r].site);
  }
  free(network->radar);
  free(network);
  list = PyList_New(0);
  PyList_Append(list,Py_BuildValue("d",rho));
  PyList_Append(list,Py_BuildValue("d",lat));
  PyList_Append(list,Py_BuildValue("d",lng));
  return list;  
}


static PyObject *
PosMag(PyRPosObject *self, PyObject *args, PyObject *kwds)
{
  PyObject *list=NULL, *timetuple=NULL;
  char *radarcode;
  struct RadarNetwork *network;
  struct Radar *radar;
  struct RadarSite *site;
  int center, bcrd, rcrd;
  int frang,rsep,rxrise,height;
  int yr,mo,dy,hr,mt;
  double sc;
  int stid;
  double rho,lat,lng;
  char *envstr=NULL;
  FILE *fp;
  int r,c;
  static char *kwlist[] = {"center","bcrd","rcrd","frang","rsep","rxrise","height", "radarcode","radarid","time",NULL};
  PyDateTime_IMPORT;
  center=0;
  bcrd=1;
  rcrd=15;
  frang=1200;
  rxrise=0;
  rsep=100;
  height=300;
  radarcode="kod";
  stid=-1;
  yr=2008;
  mo=7;
  dy=12;
  hr=12;
  mt=0;
  sc=0; 

  if (! PyArg_ParseTupleAndKeywords(args, kwds, "|iiiiiiisiO", kwlist, 
                                      &center,&bcrd,&rcrd,&frang,&rsep,&rxrise,&height,&radarcode,&stid,&timetuple))
     return NULL; 

  if ( timetuple != NULL) {
    if (PyDateTime_Check(timetuple)) {	
      yr=PyDateTime_GET_YEAR(timetuple);   
      mo=PyDateTime_GET_MONTH(timetuple);  
      dy=PyDateTime_GET_DAY(timetuple);   
      hr=PyDateTime_DATE_GET_HOUR(timetuple);   
      mt=PyDateTime_DATE_GET_MINUTE(timetuple);   
      sc=PyDateTime_DATE_GET_SECOND(timetuple);   
    }
  }
  envstr=getenv("SD_RADAR");
  if (envstr==NULL) {
    fprintf(stderr,"Environment variable 'SD_RADAR' must be defined.\n");
    exit(-1);
  }

  fp=fopen(envstr,"r");

  if (fp==NULL) {
    fprintf(stderr,"Could not locate radar information file.\n");
    exit(-1);
  }

  network=RadarLoad(fp);
  fclose(fp); 

  if (network==NULL) {
    fprintf(stderr,"Failed to read radar information.\n");
    exit(-1);
  }

  envstr=getenv("SD_HDWPATH");
  if (envstr==NULL) {
    fprintf(stderr,"Environment variable 'SD_HDWPATH' must be defined.\n");
    exit(-1);
  }

  RadarLoadHardware(envstr,network);


  if (stid==-1) {
    stid=RadarGetID(network,radarcode);
  }
  radar=RadarGetRadar(network,stid);
  site=RadarYMDHMSGetSite(radar,yr,mo,dy,hr,mt,(int) sc);
  RPosMag(center,bcrd,rcrd,site,frang,rsep,rxrise,height,&rho,&lat,&lng);
  radar=NULL;
  site=NULL;
  for (r=0;r<network->rnum;r++) {
    for (c=0;c<network->radar[r].cnum;c++) { 
      if (network->radar[r].code[c] !=NULL) free(network->radar[r].code[c]);
    } 
    if (network->radar[r].code !=NULL) free(network->radar[r].code);
    if (network->radar[r].name !=NULL) free(network->radar[r].name);
    if (network->radar[r].operator !=NULL) free(network->radar[r].operator);
    if (network->radar[r].hdwfname !=NULL) free(network->radar[r].hdwfname);
    if (network->radar[r].site !=NULL) free(network->radar[r].site);
  }
  free(network->radar);
  free(network);
  list = PyList_New(0);
  PyList_Append(list,Py_BuildValue("d",rho));
  PyList_Append(list,Py_BuildValue("d",lat));
  PyList_Append(list,Py_BuildValue("d",lng));
  return list;  
}
static PyMethodDef module_methods[] = {
   	{ "PosGeo", (PyCFunction)PosGeo , METH_KEYWORDS, NULL },
   	{ "PosMag", (PyCFunction)PosMag , METH_KEYWORDS, NULL },
   	{ "PosCubic", (PyCFunction)PosCubic , METH_KEYWORDS, NULL },
   	{ "CalcVector", (PyCFunction)CalcVector , METH_KEYWORDS, NULL },
	{ NULL, NULL, 0, NULL } /* Sentinel */
};
 
PyMODINIT_FUNC
initpyrpos(void) 
{
    PyObject* m;
    m = Py_InitModule3("pyrpos", module_methods,
                       "Module for rpos positioning");

    if (m == NULL)
      return;
}
