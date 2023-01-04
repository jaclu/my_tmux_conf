## color-line-24-bit.sh

If there are no sharp transitions, you can display 24-bit colors.

## 24-bit-colors.sh

Prints 8 lines of continuous colors. If your line is to short it wraps to the next.
This isn't an issue with your terminal, you need to have it 128 chars wide for correct displayal.

If you don't see continuous smooth color transitions, something is reducing your colors to 256
or less. mosh seems to often cause this. Try to connect with ssh first, if that works,
then mosh is the problem.

## 256-colors.sh

Prints the color names in sequence, so you can see what each color
looks like on your display.
Be aware that terminal themes might alter display of colors
