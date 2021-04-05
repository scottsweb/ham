args = {"entity_id": "vacuum.xiaomi_vacuum_cleaner", "command": "app_segment_clean", "params":[]}

lounge = data.get("input_boolean.monk_clean_lounge")
kitchen = data.get("input_boolean.monk_clean_kitchen")
bedroom = data.get("input_boolean.monk_clean_bedroom")
dining = data.get("input_boolean.monk_clean_dining")
bathroom = data.get("input_boolean.monk_clean_bathroom")
office = data.get("input_boolean.monk_clean_office")

if lounge == 'on':
  args["params"].extend([19])
if kitchen == 'on':
  args["params"].extend([16])
if bedroom == 'on':
  args["params"].extend([1])
if dining == 'on':
  args["params"].extend([18])
if bathroom == 'on':
  args["params"].extend([17])
if office == 'on':
  args["params"].extend([21])

#logger.info( args )
hass.services.call('vacuum', 'send_command', args)
