display_status.json
  Tells us what's being passed to the standard printer screen
  The *progress* field is a percentage.  In the below example .68 is %68
    {"result": {"display_status": {"progress": 0.68, "message": null}}}

extruder.json
  *target* is the temperature we've set the hotend to be.  This may be
  above the current temp if we're heating, or below if we are not actively
  heating the hotend.
  *temperature* is the current temperature to a ridiculous degree of precision
  This can probably just be treated as an integer, we don't need partial degrees

heater_bed.json
  Same formatting and data as extruder, but for heated beds.

virtual_sdcard.json
  Information about the currently printing file.
  *print_duration* is the time spent laying down plastic
  *total_duration* includes any time for pauses or filament changes.
    Typically identical to *print_duration*
  *filament_used* is amount of filament pushed through, we can use this
    as one possible way to determine remaining print time if we get the
    total filament usage over the entire print from another location
  *file_position* gives us the location (i don't know if this is in bytes
    or line number or what) of the file that we're currently printing
    could be used to determine % of print completed
  *progress* makes use of another metric to possibly estimate print time

temperature_store.json
  This is more tricky.  You have two dict elements:
    *heater_bed*
    and
    *extruder*

  each of which has two sub elements:
    *temperatures*
    and
    *targets*

  I believe each of those sub elements is populated every second, so there
    will have to be a little math done to figure out what's been going on and for how long.
  *temperatures* are actual temperatures taken and *targets* are the desired temp.

