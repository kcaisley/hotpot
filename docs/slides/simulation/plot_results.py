# plot_results.py -- measured ngspice waveforms; no synthetic waveform data.
from pathlib import Path
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
P=Path(__file__).resolve().parent;A=P.parent/'assets/extension'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':15,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#4C566A','text.color':'#4C566A','xtick.color':'#4C566A','ytick.color':'#4C566A','axes.edgecolor':'#4C566A','pdf.fonttype':42})
v=np.loadtxt(P/'inverter_waveforms.dat',skiprows=1);t=v[:,0]*1e12
colors=['#A3BE8C','#5E81AC','#BF616A','#B48EAD']
def cross(y,level,up,lo,hi):
 ids=np.where((t[:-1]>=lo)&(t[:-1]<=hi)&((y[:-1]<level)&(y[1:]>=level) if up else (y[:-1]>level)&(y[1:]<=level)))[0]
 i=ids[0];return float(t[i]+(level-y[i])*(t[i+1]-t[i])/(y[i+1]-y[i]))
a50=cross(v[:,2],.55,True,90,180);z50=cross(v[:,3],.55,False,90,200)
afall=cross(v[:,2],.55,False,390,480);zrise=cross(v[:,3],.55,True,390,490)
a30=cross(v[:,2],.33,True,90,180);a70=cross(v[:,2],.77,True,90,180)
fig,axes=plt.subplots(1,2,figsize=(13.8,5.3),sharey=True)
for ax,(lo,hi,st,en,name) in zip(axes,[(85,185,a50,z50,'tPHL'),(395,505,afall,zrise,'tPLH')]):
 for i,label in [(2,'A'),(3,'ZN'),(4,'load')]:ax.plot(t,v[:,i],label=label,c=colors[i-1],lw=2.6)
 ax.axhline(.55,c='#D8DEE9',ls='--');ax.axvline(st,c='#5E81AC',ls=':',lw=1);ax.axvline(en,c='#BF616A',ls=':',lw=1)
 ax.annotate('',xy=(en,1.04),xytext=(st,1.04),arrowprops={'arrowstyle':'<->','color':'#5E81AC','lw':1.8})
 ax.text((st+en)/2,1.12,f'{name} = {en-st:.2f} ps',ha='center',color='#5E81AC');ax.set_xlim(lo,hi);ax.set_ylim(-.03,1.26);ax.set_xlabel('Time (ps)');ax.grid(alpha=.12)
axes[0].set_ylabel('Voltage (V)');
for ax in axes:ax.legend(loc='upper right')
fig.tight_layout();fig.savefig(A/'propagation.pdf');plt.close(fig)
fig,ax=plt.subplots(figsize=(12,5.5));ax.plot(t,v[:,2],c=colors[1],lw=2.5,label='A');ax.plot(t,v[:,3],c=colors[2],lw=2.5,label='ZN')
for val,lab in [(.33,'30%'),(.55,'50%'),(.77,'70%')]:ax.axhline(val,c='#D8DEE9',ls='--');ax.text(168,val+.02,lab,color='#4C566A')
ax.annotate('',xy=(a70,.2),xytext=(a30,.2),arrowprops={'arrowstyle':'<->','color':'#5E81AC','lw':2});ax.text((a70+a30)/2,.08,f'Input slew = {a70-a30:.2f} ps',ha='center',color='#5E81AC');ax.set(xlim=(90,180),ylim=(-.03,1.2),xlabel='Time (ps)',ylabel='Voltage (V)');ax.legend(loc='upper right');fig.tight_layout();fig.savefig(A/'slew.pdf');plt.close(fig)
# Supply power is asymmetric: output charging draws from VDD, discharge uses stored energy.
fig,axes=plt.subplots(2,2,figsize=(13,5.5),sharex='col',sharey='row',gridspec_kw={'height_ratios':[1,1.3]})
energy=0
for col,(lo,hi,edge,title) in enumerate([(1050,1400,1110,'Output rises: VDD charges load'),(700,1050,800,'Output falls: load discharges')]):
 ax,bx=axes[:,col];mask=(t>=lo)&(t<=hi)
 e=np.trapz(v[mask,5],v[mask,0])*1e15;energy+=e
 for i,label in [(2,'A'),(3,'ZN')]:ax.plot(t-edge,v[:,i],c=colors[i-1],lw=2,label=label)
 ax.set_title(title,color='#5E81AC',fontsize=15,pad=12);ax.set_ylim(-.05,1.18)
 ax.legend(loc='upper right',ncol=2,fontsize=11)
 bx.plot(t-edge,v[:,5]*1e6,c='#B48EAD',lw=2);bx.fill_between(t-edge,0,v[:,5]*1e6,color='#B48EAD',alpha=.18)
 bx.set(xlim=(-30,140),ylim=(-60,420),xlabel='Time from source edge (ps)')
 bx.text(.97,.84,f'VDD energy: {e:.2f} fJ',transform=bx.transAxes,ha='right',color='#B48EAD',fontsize=13)
 print(title+f': VDD energy {e:.4f} fJ')
axes[0,0].set_ylabel('Voltage (V)');axes[1,0].set_ylabel('VDD power (µW)')
fig.tight_layout();fig.savefig(A/'power.pdf');plt.close(fig)
d=json.loads((A/'timing_table.json').read_text());fig,ax=plt.subplots(figsize=(9,5.4))
for i in [0,2,4,6]:ax.plot(d['load_ff'],np.array(d['cell_fall_ns'][i])*1000,'o-',label=f"Slew {d['input_slew_ns'][i]*1000:.1f} ps")
ax.set(xlabel='Output capacitance (fF)',ylabel='Cell fall delay (ps)');ax.legend();ax.grid(alpha=.15);fig.tight_layout();fig.savefig(A/'liberty_table.pdf');fig.savefig(A/'liberty_table.svg');plt.close(fig)
print(f'Measured tPHL={z50-a50:.3f} ps, tPLH={zrise-afall:.3f} ps; cycle energy={energy:.3f} fJ')
