data = readmatrix("TDS Data Real.xlsx")
ppm = data(:,1);
mv = data(:,2);

ppm_limit = ppm(4:end);
mv_limit = mv(4:end);

%% Polyfit
x = linspace(0,1500,100);
p = polyfit(ppm_limit,mv_limit,3);
y = polyval(p,x);

%% Plot
figure
plot(ppm_limit,mv_limit, 'x', 'LineWidth', 1.5)

hold on

plot(ppm(3),mv(3), 'x', 'LineWidth', 1.5)
plot(x,y, '--', 'LineWidth', 1.5)
%xline(1000, '--black')
txt = {'y = ' num2str(p(1)) 'x^3 + ' num2str(p(2)) 'x^2 + ' num2str(p(3)) 'x + ' num2str(p(4))}

set(gca, 'linewidth', 1.5)

ylim([0 2500])
xlabel('Concentration [ppm]')
ylabel('Voltage [mV]')
title('TDS sensor calibration')
legend('Data', 'Out of Range', 'Fit', 'Location','northwest')


