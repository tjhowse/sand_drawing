import sand_drawing
import time
while (True):
    try:
        sand_drawing.main()
    except Exception as e:
        print("Exception occurred ): {}".format(str(e)))
        time.sleep(5)
        # import machine
        # machine.reset()
