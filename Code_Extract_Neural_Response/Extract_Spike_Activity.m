
clear; close all; clc

Work_path = '/Users/chenyu/Workspace/Nuerohackason2017/';

for path_set = {'16_PLANE1','16_PLANE2','18_PLANE1','18_PLANE2'};

% load([Work_path 'Data/2105_NC_170516_PLANE1_PINKNOISE_dataOut.mat'])
% load([Work_path 'Data/2105_NC_170516_PLANE2_PINKNOISE_dataOut.mat'])
% load([Work_path 'Data/2105_NC_170518_PLANE1_PINKNOISE_dataOut.mat'])
% load([Work_path 'Data/2105_NC_170518_PLANE2_PINKNOISE_dataOut.mat'])

load([Work_path 'Data/2105_NC_1705' path_set{1} '_PINKNOISE_dataOut.mat'])


% Trial_Num = 1; % 1-16

Response_Neuron_Ind = dataOut.stats.global.responsive_cells_p005_fdr_average; 


for TaskType = 1:4; % 1-4
for Neuron_Num = 1:size(dataOut.trial(1).signal, 1); % 1-around 320

PSTH = [];
for trial_ind = 1:16
for repetition_ind = 1:17
    
segment_index = dataOut.trial(trial_ind).stimulus_vector == TaskType & dataOut.trial(trial_ind).repetition_vector == repetition_ind;
PSTH = padconcatenation(PSTH, dataOut.trial(1).signal_deconv(Neuron_Num, segment_index), 1);

end
end

PSTH = nanmean(PSTH);

% save([Work_path 'Spike_Response_mat/D16P1T' num2str(TaskType) '_N' num2str(Neuron_Num) '.mat'], 'PSTH')
csvwrite([Work_path 'Spike_Response_csv_whole2/Day' path_set{1} 'Task' num2str(TaskType) '_Neuron' num2str(Neuron_Num) '.csv'], PSTH)
end
end
end





