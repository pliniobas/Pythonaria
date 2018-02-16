Spectrum.m:
clear;
clc;
%define basic variables
Rho=1000;
g=9.81;
Avolt=254; %Calibration value A of the pressure meter
Bvolt=-43250; %Calibration value B of the pressure meter
load rawdata.txt;
%transformation from Volts to pressure using calibration constants Avolt
%and Bvolt
%Avolt has dimension Pa/V, Bvolt has dimension Pa
P=Avolt*rawdata+Bvolt;
%interval is the sample frequency interval of the sensor
interval=.25;
n=numel(rawdata); %count number of samples
tottime=n*interval; %calculate total duration of observation in sec
ttime=(interval:interval:tottime); %create array with time
time=ttime.'; %change orientation of matrix
% calculate regression coefficients to compensate for change in waterlevel
% during the observations
%plot(time,rawdata);
%plot(time,P);
BB=polyfit(time,P,1); %regression analysis to determine real waterdepth at
any moment
%and correct for hydrostatic pressure
Intercept=BB(2);
Slope=BB(1);
Pwave=P-Intercept-time*Slope;
Pstatic=P-Pwave; %Hydrostatic pressure
depth=mean(Pstatic/Rho/g);
%===================================================================
% simple script utilizing crosgk (by G. Klopman) to obtain
% spectral estimate
%===================================================================
% data contains the data
% N is the number of samples per data segment (power of 2)
% M is the number of frequency bins over which is smoothed (optional),
% no smoothing for M=1 (default)
% DT is the time step (optional), default DT=1
% DW is the data window type (optional): DW = 1 for Hann window (default)
% DW = 2 for rectangular window
% stats : display resolution, degrees of freedom (optimal, YES=1, NO=0)
%
% Output:
% P contains the (cross-)spectral estimates: column 1 = Pxx, 2 = Pyy, 3 =
Pxy
% F contains the frequencies at which P is given load time series
M = 100; %higher values of M give more smoothing of the spectrum
DT = interval;
data = Pwave;
[P,F,dof]=crosgk(data,data,length(data),M,DT,1,0);
%plot the pressure spectrum
%figure
%plot(F,P(:,1)) % F is pressure^2/Hz
%axis ([0 0.3 0 1500])
%axis 'auto y'
H.P. Winde 17 June 2012
Page | XI
%xlabel('frequency [Hz]');
%ylabel ('pressure Pa^2/Hz');
%recalcultate pressure spectrum to energy spectrum
eta=1:length(F); % length (F) is number of frequency bins
for i=1:length(F)
eta(i)=0;
end;
m0=0; %zero-th moment
m1=0; %first moment
m2=0; %second moment
m01=0; %first negative moment {m(-1,0)}
deltaF= F(31)-F(30);
upgrade=1.00; %calabration coeffectien for transformation pressure to height
emax=0;
% claculation loop to transform pressure spectrum to energy spectrum and
% to calculate the moments of the spectrum
% low and high frequencies are deleted, range from 200 to 0.2*max
% frequency bin, 200 means f= 200*deltaF, which is approx. 30 seconds
% 0.2*length(F)*deltaF = 0.4, so Tmin - 2.5 seconds
for i=20:0.20*length(F)
T=1/F(i);
pr=sqrt(P(i,1)); %pr=pressure value in pressure spectrum
L0=1.56*T*T;
if (depth/L0<0.36)
L=sqrt(g*depth)*(1-depth/L0)*T;
else
L=L0;
end;
e=(upgrade*pr/(Rho*g)*cosh(2*pi/L*depth))^2; %e=energiedichtheid in Hz/m2
eta(i)=e; %replacing pressure value to energy value in spectrum
if e>emax
emax=e;
Tpeak=T;
end;
m0 =m0 +e*deltaF;
m1 =m1 +e*deltaF*F(i);
m2 =m2 +e*deltaF*F(i)^2;
m01=m01+e*deltaF/F(i);
end;
m0
Hm0=4*sqrt(m0) %one may assume Hs = Hm0
Hrms=sqrt(8*m0)
Tm=sqrt(m0/m2)
T01=m0/m1
T10=m01/m0 %Period based on first negative moment
Tpeak % peak period
figure
plot(F,eta)
axis([0.06 0.4 0 10000])
axis 'auto y'
xlabel('frequency [Hz]');
ylabel ('Energy m^2/Hz');