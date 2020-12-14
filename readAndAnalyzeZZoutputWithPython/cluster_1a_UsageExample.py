import zebrazoom
import pickle

# Creating the dataframe on which the clustering will be applied

dataframeOptions = {
  'pathToExcelFile'                   : '../zebrazoom/dataanalysis/experimentOrganizationExcel/',
  'fileExtension'                     : '.xls',
  'resFolder'                         : '../zebrazoom/dataanalysis/data',
  'nameOfFile'                        : 'example',
  'smoothingFactorDynaParam'          : 0,   # 0.001
  'nbFramesTakenIntoAccount'          : -1, #28,
  'numberOfBendsIncludedForMaxDetect' : -1,
  'minNbBendForBoutDetect'            : 3,
  'defaultZZoutputFolderPath'         : '../zebrazoom/ZZoutput/',
  'computeTailAngleParamForCluster'   : True,
  'computeMassCenterParamForCluster'  : True
}

[conditions, genotypes, nbFramesTakenIntoAccount] = zebrazoom.createDataFrame(dataframeOptions)


# Applying the clustering on this dataframe

clusteringOptions = {
  'analyzeAllWellsAtTheSameTime' : 0, # put this to 1 for head-embedded videos, and to 0 for multi-well videos
  'pathToVideos' : '../zebrazoom/ZZoutput/',
  'nbCluster' : 3,
  'modelUsedForClustering' : 'KMeans', # put either 'KMeans' or 'GaussianMixture' here
  #'nbPcaComponents' : 30,
  'nbFramesTakenIntoAccount' : nbFramesTakenIntoAccount,
  'scaleGraphs' : True,
  'showFigures' : False,
  'useFreqAmpAsym' : False,
  'useAngles' : False,
  'useAnglesSpeedHeadingDisp' : False,
  'useAnglesSpeedHeading' : True,
  'useAnglesSpeed' : False,
  'useAnglesHeading' : False,
  'useAnglesHeadingDisp' : False,
  'useFreqAmpAsymSpeedHeadingDisp' : False,
  'videoSaveFirstTenBouts' : False,
  'globalParametersCalculations' : True,
  'nbVideosToSave' : 10,
  'resFolder' : '../zebrazoom/dataanalysis/data',
  'nameOfFile' : 'example'
}


# Applies the clustering for the first time
[allBouts, classifier] = zebrazoom.applyClustering(clusteringOptions, 0, '../zebrazoom/dataanalysis/resultsClustering')


# Saves the classifier
outfile = open('../zebrazoom/dataanalysis/classifiers/classifier_' + clusteringOptions['nameOfFile'] + '.txt','wb')
pickle.dump([classifier, nbFramesTakenIntoAccount],outfile)
outfile.close()
