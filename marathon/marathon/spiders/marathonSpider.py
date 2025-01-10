import scrapy
import csv
import json

class MarathonspiderSpider(scrapy.Spider):
    name = "marathonSpider"
    
    start_urls = [
        'https://www.marathonarcorewards.com/ajax_trip_planner_search.html?reason=get-station-info'
    ]
    
    def parse(self, response):
        # Parse the JSON response
        data = json.loads(response.body)

        # Open CSV file to write the data
        with open('marathon_stations.csv', 'w', newline='', encoding='utf-8') as csvfile:
            # Start with fixed columns
            fieldnames = [
                'item_id', 'item_name', 'addr1', 'state', 'lat', 'lng', 'phone', 'directions', 'site_brand'
            ]
            
            # Dynamically add description and unitPrice columns
            max_price_entries = 10  # Adjust this number if needed
            for i in range(1, max_price_entries + 1):
                fieldnames.append(f'description_{i}')
                fieldnames.append(f'unitPrice_{i}')
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Iterate through each station in the JSON data
            for station in data:
                row = {
                    'item_id': station.get('item_id'),
                    'item_name': station.get('item_name'),
                    'addr1': station.get('addr1'),
                    'state': station.get('state'),
                    'lat': station.get('lat'),
                    'lng': station.get('lng'),
                    'phone': station.get('phone'),
                    'directions': station.get('directions'),
                    'site_brand': station.get('site_brand')
                }

                # Extract the price data (description and unit price)
                price_data = station.get('price_data', [])
                
                # Add descriptions and unit prices to the row dynamically
                for i, price in enumerate(price_data):
                    description_key = f'description_{i+1}'
                    unit_price_key = f'unitPrice_{i+1}'
                    row[description_key] = price.get('description')
                    row[unit_price_key] = price.get('unitPrice')

                # Write the row to the CSV file
                writer.writerow(row)
