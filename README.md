# idler

Code to automatically play Idle Champions

## Disclaimer

This is just a fun little project, which probably won't help anyone. If you want to use this code note:
 * It will be buggy
 * Much of the code is a hack to try and get some stability without fully diagnosing the game state
 * You will need to be able to code to get it to work
 * To get started you need your own image reference, using acquire_images.py.
 * I wasn't careful with writing decent code.

## Getting started

Very roughly:
 * Install the environment (using the environment.yml file if you use conda), I believe you also have to pip install pytesseract.
 * Update `locations.py`. You will need to for some set resolution you want to run at find the exact positions of all the buttons you are going to automatically get the program to click. You see I have two setups for a fullscreen and a windowed version of the game.
 * The lvl checking run by checking image matches with the base lvl number. So you need to use acquire_images.py to make those base images to check against. You need to do this for "undone" and "done" levels.
 * Try running some tests. You will surely want to build your own loop, similar to the loops I have in `farm.py`.
 * Debug and have fun.

## Automated Briv gem farming

The general idea will be the following:

### In game setup:
  * Speed/DPS + briv formation saved as 'w'
  * Briv stacking formation (probably just briv) saved on 'e'
  * Modron set to
    - Start with speed formation
    - Use any pots desired (I assume some speed, and maybe a click dmg)
    - modron reset set to some lvls above a stack area

### Program:
```
ic = Idler('windowed_hermes')                   # Init the class
ic.alt_tab()                                    # alt-tab to IC
while True:
    ic.wait_for_base_lvl(936, stop_at_lvl=True) # Stop lvl a few lvls above reset on modron
    ic.select_group('e')                        # Switch to briv formation
    ic.click_back()                             #
    ic.click_level(3)                           # This and the prev step can go to a lvl with ranged
    ic.wait_for_enrage()                        # Get some stacks (usually about 3k by enrage time)
    ic.wait(5)                                  # If additional stacks needed
    ic.swap_to_group_and_start_progress('w')    # Swap to the speed formation, and continue progress to reset lvl
    ic.wait_for_reset()                         # Wait until we see lvl '1' again (i.e. have started a new run)
    ic.print_run_stats(num_bosses=189)          # Print some stats. You need to work out yourself how many bosses you do
```

## Idler setups:
    True: 1920x1080, 75% UI, fullscreen.
    False: 1080x720, 100% UI, in upper right corner

## Known bugs / improvement ideas:
    * ic.press_start_stop() just presses 'g', should ideally check ig the
      'go' button is green first and then either start or stop depending what
      you want.
    * ic.swap_to_group_and_start_progress('w') doesn't always select the group
      correctly, thus the code presses 'w' many times. Don't understand this.
    * I believe if we get a server error this will cause it to no longer find
      lvls in ic.wait_for_base_lvl(#) and thus will overshoot the reset
      without stacking, getting into stackless looping.