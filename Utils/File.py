import json
import time

class File:

    @staticmethod
    def writeToFile(Config, Recombination, Problem, StatBestByRun, StatAvgBestByRun):
        timestamp = time.gmtime()
        timestamp = '' + str(timestamp.tm_mday) + '_' + str(timestamp.tm_hour) + '_' + str(timestamp.tm_min)

        fileName = \
            Problem['name'] + "_" + \
            Recombination['name'] + "_" + \
            str(Problem['config']['cromo_size']) + "_" + \
            timestamp

        path = 'Results/'
        f = open(path + fileName + ".txt", 'w')

        num = json.dumps({'Num_generations': Config['numb_generations']})
        pop = json.dumps({'Pop_size': Config['pop_size']})
        run = json.dumps({'Runs': Config['runs']})
        statBest = json.dumps({'StatBestByRun': StatBestByRun})
        statAvg = json.dumps({'StatAvgBestByRun': StatAvgBestByRun})

        f.write(
            num + "\n" +
            pop + "\n" +
            run + "\n" +
            statBest + "\n" +
            statAvg + "\n")

        f.close()