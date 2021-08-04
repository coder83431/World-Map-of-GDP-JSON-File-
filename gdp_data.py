import json
import pygal
from pygal.maps.world import World
from pygal.style import LightColorizedStyle as LCS, RotateStyle as RS


from country_codes import get_country_code
# Load the data into a list.
filename = "/Users/tgiedraitis/Downloads/gdp-master/data.json"
with open(filename) as f:
    gdp_data = json.load(f)

# Build a dictionary of gdp data.
cc_gdps = {}
for gdp_dict in gdp_data:
    if gdp_dict['Year'] == '2014':
        country_name = gdp_dict['Country Name']
        gdp = int(float(gdp_dict['Value']))
        code = get_country_code(country_name)

        if code:
            print(code + ":" + str(gdp))
            cc_gdps[code] = gdp
        else:
            print("Error:", country_name)

# Group the countries into 3 gdp levels.
#  Less than 5 billion, less than 50 billion, >= 50 billion.
#  Also, convert to billions for displaying values.
cc_gdps_1, cc_gdps_2, cc_gdps_3 = {}, {}, {}
for cc, gdp in cc_gdps.items():
    if gdp < 5000000000:
        cc_gdps_1[cc] = round(gdp / 1000000000)
    elif gdp < 50000000000:
        cc_gdps_2[cc] = round(gdp / 1000000000)
    else:
        cc_gdps_3[cc] = round(gdp / 1000000000)



print(len(cc_gdps_1)), print(len(cc_gdps_2)), print(len(cc_gdps_3))


wm = pygal.maps.world.World()
wm_style = RS('#994033', base_style = LCS)
wm = World(style=wm_style)
wm.title = "World GDP in 2014 By Country"
wm.add("0-5bn", cc_gdps_1)
wm.add("<50bn", cc_gdps_2)
wm.add(">=50bn", cc_gdps_3)
wm.add("2014", cc_gdps)
wm.render_in_browser()
