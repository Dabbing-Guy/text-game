## About Maps

Maps have two parts:
- `.map` - Stores the actual map that will be drawn to the terminal
- `.mapdata` - Stores the behind the scenes data about the map. Used to know when things should happen in relation to the map. It must be the same size as its corresponding `.map` file

## `.mapdata` supported symbols

` ` - Nothing special. 
`#` - Wall. Means player character can not go there
`e` - Exit. This means the game should jump to next map
`S` - Player start location
`%` - Interactable 1

