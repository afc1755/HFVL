# HFVL
Hash Function Visualization Language

Created by Andrew Chabot
Advisor: Dr. Hans-Peter Bischof

A simple to use language called the Hash Function Visualization Language or HFVL.
This repository contains all necessary files for created and running files in the language.
There are also visualizations created in the language for SHA-1, SHA-2 256 and SHA-3 256 available in this repository.
These are called *SHA1*, *SHA2*, and *SHA3* respectively. All of these files link to additional subvisualization files,
which are also included in this repository.

## Usage
To run HFVL on a file, simply run the main HFVL.py file. On input you will get a message to input a file.
> Enter HFVL filename to run: 

If you enter an HFVL file, you should get a message that looks like
> file found, loading visualization for: *SHA1*


## Language Syntax
The SHA visualizations serve as examples on how to use HFVL. The syntax of HFVL is somewhat unique, but simplistic in nature.

### Frames

All the visual changes occur within Frames.

Every frame is started with a Frame : command and ended with a Frame End command. A sample frame statement is below.

> Frame 1:
>
> Frame Changes
>
> Frame End

## Visual Functions

The visual functions are below with examples:

###$drawBox or $db

The $drawBox function takes in 5 parameters and has 4 optional parameters.

> $drawBox(box_id, x, y, width, height, color=, bold=, text=, link=, input=)
>
> $drawBox(box1, 100, 100, 100, 100, color=blue, bold=True, text='this is box1', link='linkfile', input=box2;box3)

The box_id parameter will be the unique identification for the box being drawn. This id will be referenced when using the $modifyBox function or the $drawArrow function.

The x and y coordinates and width and height are used for determining the position and size of the box being drawn. These are necessary paremeters.

The optional parameters are color, bold, link, and input. All of these parameters require you to use the format 'parameter=' when setting them.

The options for color are 'blue', 'red', 'green', and 'black'. 'black' is the default color.

The options for bold are True and False.

The text parameter can be any valid text characters. This text will be displayed inside of the box, centered if fitting on one line and paragraph style if multi-line.

For link, the input must be the name of another HFVL filename to be used for subvisualization.

For input, the input must be the id of a current box. Multiple box ids can be provided but must be seperated by a semicolon.

###$drawArrow or $da

The $drawArrow function takes in 2 parameters and has 2 optional parameters.

> $drawArrow(start_box_id, end_box_id, color=, bold=)
>
> $drawArrow(box1, box2, color=red, bold=False)

The input parameters start_box_id and end_box_id must correspond to valid boxes to draw an arrow between. The function will pathfind and draw an arrow that begins at start_box_id and ends at end_box_id. These ids will create the id for the arrow.

The color and bold parameters have the same valid values as mentioned in $drawBox.

###$modifyBox or $mb

The $modifyBox function takes in 1 parameter and has 5 optional parameters. This function is used to change the optional parameters of a box.

> $modifyBox(box_id, color=, bold=, text=, link=, input=)
>
> $modifyBox(box1, color=red, bold=False, link='linkfile2', input=box2)

The parameters are identical to those in the $drawBox function. If a new link is given, the old link will be removed. If a new input is given, the old inputs will be removed and replaced with the new input.

###$modifyArrow or $ma

The $modifyArrow function takes in 2 parameters and has 2 optional parameters. This function is used to change the optional parameters of an arrow.

> $modifyArrow(start_box_id, end_box_id, color=, bold=)
>
> $modifyArrow(box1, box2, color=green, bold=True)

The function takes in two box_ids as the id for the arrow to modify. The color and bold parameters can then be changed.

###$resetBox or $rb

The $resetBox command is a shortcut to set a box back to default settings. This means the box will have links and inputs removed, the box will have bold set to False, the color of the box will be 'black'. **The text of the box will not be modified**.
> $resetBox(box_id)
>
> $resetBox(box1)


###$resetArrow or $ra

The $resetArrow command is a shortcut to set an arrow back to default settings. This means the arrow will have bold set to False, and the color of the arrow will be 'black'.
> $resetArrow(start_box_id, end_box_id)
>
> $resetArrow(box1, box2)

###$modifyTitle or $mt

The $modifyTitle command has three optional parameters and is used to change the attributes for the title of the visualization.

> $modifyTitle(text=,color=)
>
> $modifyTitle(text='Sample Visualization', color='red')


## Variables
Variables can be used to store string and integer values. All variables must begin with an underscore symbol and must be given a value on declaration.
String variables should not use quotation marks.

> _stringvar = sample text
>
> _intvar = 0 


## Non-Drawing Functions
Non-drawing functions are used to modify text and variables. All of these functions begin with an @ symbol. Arguments in these functions must be seperated with a semicolon(;). These functions are listed below:

> @bytebit(bytes) - returns converted input byte text into bits
>
> @bitbyte(bits) - returns converted input bit text into bytes
> 
> @lbitshift5(bits) - left bit shifts input bits by 5 and returns result
>
> @lbitshift30(bits) - left bit shifts input bits by 30 and returns result
>
> @rbitshift2(bits) - right bit shifts input bits by 2 and returns result
> 
> @rbitshift13(bits) - right bit shifts input bits by 13 and returns result
>
> @rbitshift22(bits) - right bit shifts input bits by 22 and returns result
>
> @rbitshift6(bits) - right bit shifts input bits by 6 and returns result
> 
> @rbitshift11(bits) - right bit shifts input bits by 11 and returns result
>
> @rbitshift25(bits) - right bit shifts input bits by 25 and returns result
>
> @rbitshift(bits;amount_to_shift) - right bit shifts input bits by input amount and returns result
>
> @not(bits) - returns the output of NOT operation on the input bits
> 
> @mod32(bits) - returns the input bits modulo 2^32
>
> @trunc32(bytes) - returns the first 32 bytes of the input bytes
>
> @first272(bytes) - returns the first 272 bytes of the input bytes
>
> @last128(bytes) - returns the last 128 bytes of the input bytes
>
> @last384(bytes) - returns the last 384 bytes of the input bytes
>
> @xorloop(a_block_bytes;d_block_bytes) - returns the output of the XORLoop part of the Keccak-f[1600] Theta function being run on the input bytes
>
> @cfunc(bytes) - returns the output of the C function part of the Keccak-f[1600] Theta function being run on the input bytes
>
> @dfunc(bytes) - returns the output of the D function part of the Keccak-f[1600] Theta function being run on the input bytes
>
> @theta(bytes) - returns the output of the Keccak-f[1600] Theta function being run on the input bytes
>
> @rho(bytes) - returns the output of the Keccak-f[1600] Rho function being run on the input bytes
>
> @pi(bytes) - returns the output of the Keccak-f[1600] Pi function being run on the input bytes
>
> @chi(bytes) - returns the output of the Keccak-f[1600] Chi function being run on the input bytes
> 
> @iota(bytes) - returns the output of the Keccak-f[1600] Chi function being run on the input bytes
>
> @kf1600(capacity;rate) - returns the output of the Keccak-f[1600] function being run on the input capacity and rate
>
> @add(bits1;bits2) - returns the sum of the two input bit blocks
>
> @and(bits1;bits2) - returns the result of the AND operation on the two input bit blocks
>
> @or(bits1;bits2) - returns the result of the OR operation on the two input bit blocks
>
> @xor(bits1;bits2) - returns the result of the XOR operation on the two input bit blocks
>
> @indexarr(array;index) - converts the input string into an array and returns the value in the given index of the array
>
> @indexmat(matrix;row;col) - converts the input string into an matrix and returns the value in the given row and column of the matrix
>
> @+(num1;num2) - returns the sum of the two input numbers
>
> @-(num1;num2) - returns the difference of the two input numbers
>
> @*(num1;num2) - returns the product of the two input numbers
>
> @mod(num1;num2) - returns the first input number modulo the second input number
>
> @lt(num1;num2) - returns True if num1 is less than num2, returns False otherwise
>
> @concat(string1;string2) - returns the string concatenation of the input strings
>

These functions can be nested within each other, an example of them being nested in SHA-1 is below for an F function:

> $modifyBox(f,text=@bitbyte(@or(@or(@bytebit(*w2);@bytebit(*w3));@and(@not(@bytebit(*w2));@bytebit(*w4)))))
>
>

## If Statements
If statements begin with a if and a function that evaluates to a boolean. Currently the @lt function is the only function that serves this purpose. 'elif' can be used for additional if statements and 'else' can also be used.

All if statements must end with an 'if end' line.

>      if @lt(_roundCount;4):
>          $mb(box1,color=blue)
>      elif @lt(_roundCount;8):
>          $mb(box1,color=green)
>      else:
>          $mb(box1,color=red)
>      if end
>
## While Statements
While loops begin with a while and then a function that evaluates to a boolean. Currently the @lt function is the only function that serves this purpose.

While loops must end with a 'while end' line.

>      while @lt(_roundNum;25):
>          _roundNum = @+(_roundNum;1)  
>      while end