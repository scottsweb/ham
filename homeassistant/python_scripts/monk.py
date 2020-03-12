args = {"entity_id": "vacuum.xiaomi_vacuum_cleaner", "command": "app_segment_clean", "params":[]}

lounge = data.get("input_boolean.monk_clean_lounge")
kitchen = data.get("input_boolean.monk_clean_kitchen")
bedroom = data.get("input_boolean.monk_clean_bedroom")
hall = data.get("input_boolean.monk_clean_hall")
gemma = data.get("input_boolean.monk_clean_office_gemma")
scott = data.get("input_boolean.monk_clean_office_scott")

if lounge == 'on':
  args["params"].extend([18])
if kitchen == 'on':
  args["params"].extend([17])
if bedroom == 'on':
  args["params"].extend([16])
if hall == 'on':
  args["params"].extend([19])
if gemma == 'on':
  args["params"].extend([20])
if scott == 'on':
  args["params"].extend([21])

#logger.info( args )
hass.services.call('vacuum', 'send_command', args)
