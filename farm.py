from idler import Idler

'''
--------------------------------------------------------------------------
Automated Briv gem farming

--------------------------------------------------------------------------
The general idea will be the following:

---- In game setup:
  * Speed/DPS + briv formation saved as 'w'
  * Briv stacking formation (probably just briv) saved on 'e'
  * Modron set to
    - Start with speed formation
    - Use any pots desired (I assume some speed, and maybe a click dmg)
    - modron reset set to some lvls above a stack area

---- Program:
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

--------------------------------------------------------------------------
Idler setups:
    True: 1920x1080, 75% UI, fullscreen.
    False: 1080x720, 100% UI, in upper right corner

--------------------------------------------------------------------------
Known bugs / improvement ideas:
    * ic.press_start_stop() just presses 'g', should ideally check ig the
      'go' button is green first and then either start or stop depending what
      you want.
    * ic.swap_to_group_and_start_progress('w') doesn't always select the group
      correctly, thus the code presses 'w' many times. Don't understand this.
    * I believe if we get a server error this will cause it to no longer find
      lvls in ic.wait_for_base_lvl(#) and thus will overshoot the reset
      without stacking, getting into stackless looping.

'''

# --------------------------------------------------------------------------
# Main program
# --------------------------------------------------------------------------

# Init the idler class:
ic = Idler('windowed_hermes', reset_lvl=995, note='Waterdeep detours')

ic.print_major_seperator()
ic.print_major_seperator()
ic.print_major("Starting running")

ic.print_major("Switching to Idle Champions")
ic.alt_tab()
ic.move_mouse_to_safe()

# ---- Simple non-reset loop:
# Adventure: Waterdeep detours
# Reset: 995 (stop 986)
# Need a click dmg pot.
ic.print_major("Starting main loop")
while True:
    ic.zero_run_clock()
    ic.wait_for_base_lvl(986, stop_at_lvl=True)
    # Switch to briv and find a nice lvl to stack on:
    ic.select_group('e')
    ic.click_back()
    ic.click_level(3)
    ic.wait(0.2)
    ic.select_group('e')
    ic.click_level(3)
    ic.wait(0.2)
    ic.click_level(3)
    # Get stacks:
    ic.wait_for_enrage()
    ic.wait(5)
    # Run to finish:
    ic.swap_to_group_and_start_progress('w')
    ic.wait_for_reset()
    # Tidy up:
    ic.print_run_stats()
    ic.increment_run_count()

# # ---- GF with GAME reset:
# # THIS WON'T WORK FOR ME IN A WINDOWED VERSION.
# # Adventure: ER?
# # Reset: 1360 (stop 500)
# # Need a click dmg pot.
# ic.print_major("Starting main loop")
# while True:
#     ic.zero_run_clock()
#     ic.wait_for_base_lvl(501, stop_at_lvl=True)
#     # Switch to briv and find a nice lvl to stack on:
#     ic.select_group('e')
#     ic.click_back()
#     ic.click_level(3)
#     ic.wait(0.2)
#     ic.select_group('e')
#     ic.click_level(3)
#     ic.wait(0.2)
#     ic.click_level(3)
#     # Get stacks:
#     ic.restart_ic()
#     # Run to finish:
#     ic.swap_to_group_and_start_progress('w')
#     ic.wait_for_reset()
#     # Tidy up:
#     ic.print_run_stats()
#     ic.increment_run_count()


# # ---- 652 Normal GF helping:
# ic.print_major("Starting main loop")
# while True:
#     ic.zero_run_clock()
#     ic.wait_for_base_lvl(986, stop_at_lvl=True)
#     ic.select_group('e')
#     ic.wait_for_enrage()
#     ic.wait(10)
#     ic.swap_to_group_and_start_progress('w')
#     ic.wait_for_reset()
#     ic.print_run_stats(num_bosses=131)
#     ic.increment_run_count()
