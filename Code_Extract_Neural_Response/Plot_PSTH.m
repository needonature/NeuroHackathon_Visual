
clear; close all; clc

Work_path = '/Users/chenyu/Workspace/Nuerohackason2017/';

% load([Work_path 'Data/2105_NC_170516_PLANE1_PINKNOISE_dataOut.mat'])
% load([Work_path 'Data/2105_NC_170516_PLANE2_PINKNOISE_dataOut.mat'])
% load([Work_path 'Data/2105_NC_170518_PLANE1_PINKNOISE_dataOut.mat'])
load([Work_path 'Data/2105_NC_170518_PLANE2_PINKNOISE_dataOut.mat'])

TaskType = 1; % 1-4
Trial_Num = 1; % 1-16

Response_Neuron_Ind = dataOut.stats.global.responsive_cells_p001_fdr_average; 

%------------ task onset and offset ----------------
% figure
% plot(dataOut.trial(Trial_Num).stimOnset, ones(1,68), 'o')
% hold on
% plot(dataOut.trial(Trial_Num).stimOffset, ones(68,1), 'x')


%------------ PSTH ----------------
% stimulus_vector
% repetition_vector 



for Neuron_Num = 1:400; % 1-around 300
PSTH = [];

for trial_ind = 1:16
for repetition_ind = 1:17
    
segment_index = dataOut.trial(trial_ind).stimulus_vector == 1 & dataOut.trial(trial_ind).repetition_vector == repetition_ind;
PSTH = padconcatenation(PSTH, dataOut.trial(1).signal_deconv(Neuron_Num, segment_index), 1);

save([Work_path 'Output/P2D18_N' num2str(Neuron_Num) '.mat'], 'PSTH')
end
end
end

% PSTH = nanmean(PSTH);
% 
% figure,
% stem(PSTH')




