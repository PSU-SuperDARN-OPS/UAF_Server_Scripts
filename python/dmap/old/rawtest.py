import rawacf
jefscan=rawacf.RawACF('/home/jspaleta/Desktop/20070723.2100.12.kod.rawacf')
normscan=rawacf.RawACF('/home/jspaleta/Desktop/20070723.2200.19.kod.rawacf')
jkey=jefscan.times[31]
nkey=normscan.times[4]
print jefscan.bmnum[jkey],normscan.bmnum[nkey]
jitem=jefscan.slist[jkey][28]
nitem=normscan.slist[nkey][40]
print jitem,nitem

figure()
jracf=jefscan.get_realacf(jkey,jitem)
jiacf=jefscan.get_imacf(jkey,jitem)
plot(jracf)
plot(jiacf)

figure()
nracf=normscan.get_realacf(nkey,nitem)
niacf=normscan.get_imacf(nkey,nitem)
plot(nracf)
plot(niacf)
show()
