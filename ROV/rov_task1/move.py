class Move:
    class Linear:
        def up():
            print("vehicle going up 1 unit")
        def down():
            print("vehicle going down 1 unit")
        def left():
            print("vehicle going left 1 unit")
        def right():
            print("vehicle going right 1 unit")
        def forward():
            print("vehicle going forward 1 unit")
        def backward():
            print("vehicle going backward 1 unit")
    class Spin:
        def axis_x_positive():
            print("vehicle turning around x axis 1 unit to positive direction")
        def axis_y_positive():
            print("vehicle turning around y axis 1 unit to positive direction")
        def axis_z_positive():
            print("vehicle turning around z axis 1 unit to positive direction")
        def axis_x_negative():
            print("vehicle turning around x axis 1 unit to negative direction")
        def axis_y_negative():
            print("vehicle turning around y axis 1 unit to negative direction")
        def axis_z_negative():
            print("vehicle turning around z axis 1 unit to negative direction")

# positive directions obey the right-hand rule.