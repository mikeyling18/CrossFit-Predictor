import get_benchmarks
import predict
import get_wod
import adjust_alpha
import read_amrap_wod_history
import get_prediction


'''
This is the main function for the entire WOD Predict program. 
'''
def main():
    newAthlete = input('Are you a new athlete? (Y/N)\n')
    if newAthlete is 'Y':
        print('Welcome to WOD-Predict!\n'
              'There are a few steps we need to complete before we get started...\n'
              'First, we will need to record your benchmark WOD scores\n')
        get_benchmarks.getBenchmarks()
        print("Wonderful! Now we can start predicting your WOD performance\n"
              "The next time you run the app, you can say you are NOT a new athlete\n")

    else:
        print("Welcome back dude/dudett! What's the WOD?\n")
        get_prediction.new_wod_prediction()


if __name__ == "__main__":
    main()