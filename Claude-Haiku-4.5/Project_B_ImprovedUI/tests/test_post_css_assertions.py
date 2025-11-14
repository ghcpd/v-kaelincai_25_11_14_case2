import pytest
import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright
import time

# Add server module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))
from server_post import TaskListImprovedServer

class TestImprovedCSS:
    def __init__(self):
        self.server = None
        self.browser = None
        self.context = None
        self.page = None
        self.css_results = {}
        
    async def setup(self):
        """Setup server and browser for CSS testing"""
        self.server = TaskListImprovedServer(port=8081)
        self.server.start()
        
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        
        await self.page.goto('http://localhost:8081')
        await self.page.wait_for_load_state('networkidle')
    
    async def teardown(self):
        """Cleanup resources"""
        if self.browser:
            await self.browser.close()
        if self.server:
            self.server.stop()
    
    async def test_task_card_properties(self):
        """Test improved task card CSS properties"""
        print("Testing improved task card CSS properties...")
        
        card_selector = '.task-card'
        cards = await self.page.query_selector_all(card_selector)
        
        if cards:
            card = cards[0]
            
            # Get computed styles
            padding = await card.evaluate('(el) => getComputedStyle(el).padding')
            margin = await card.evaluate('(el) => getComputedStyle(el).marginBottom') 
            border_radius = await card.evaluate('(el) => getComputedStyle(el).borderRadius')
            box_shadow = await card.evaluate('(el) => getComputedStyle(el).boxShadow')
            
            self.css_results['task_card'] = {
                'padding': padding,
                'margin': margin,
                'border_radius': border_radius,
                'box_shadow': box_shadow
            }
    
    async def test_improved_typography_properties(self):
        """Test improved typography CSS properties"""
        print("Testing improved typography properties...")
        
        # Task title
        title_element = await self.page.query_selector('.task-title')
        if title_element:
            font_size = await title_element.evaluate('(el) => getComputedStyle(el).fontSize')
            font_weight = await title_element.evaluate('(el) => getComputedStyle(el).fontWeight')
            line_height = await title_element.evaluate('(el) => getComputedStyle(el).lineHeight')
            color = await title_element.evaluate('(el) => getComputedStyle(el).color')
            
            self.css_results['task_title'] = {
                'font_size': font_size,
                'font_weight': font_weight,
                'line_height': line_height,
                'color': color
            }
        
        # Task description
        desc_element = await self.page.query_selector('.task-description')
        if desc_element:
            font_size = await desc_element.evaluate('(el) => getComputedStyle(el).fontSize')
            color = await desc_element.evaluate('(el) => getComputedStyle(el).color')
            
            self.css_results['task_description'] = {
                'font_size': font_size,
                'color': color
            }
    
    async def test_improved_button_properties(self):
        """Test improved button CSS properties"""
        print("Testing improved button properties...")
        
        # Primary button
        btn_primary = await self.page.query_selector('.btn-primary')
        if btn_primary:
            bg_color = await btn_primary.evaluate('(el) => getComputedStyle(el).backgroundColor')
            border_radius = await btn_primary.evaluate('(el) => getComputedStyle(el).borderRadius')
            padding = await btn_primary.evaluate('(el) => getComputedStyle(el).padding')
            font_size = await btn_primary.evaluate('(el) => getComputedStyle(el).fontSize')
            min_height = await btn_primary.evaluate('(el) => getComputedStyle(el).minHeight')
            
            self.css_results['btn_primary'] = {
                'background_color': bg_color,
                'border_radius': border_radius,
                'padding': padding,
                'font_size': font_size,
                'min_height': min_height
            }
            
            # Test improved hover state
            await self.page.hover('.btn-primary')
            await asyncio.sleep(0.2)  # Wait for transition
            
            hover_bg_color = await btn_primary.evaluate('(el) => getComputedStyle(el).backgroundColor')
            hover_box_shadow = await btn_primary.evaluate('(el) => getComputedStyle(el).boxShadow')
            hover_transform = await btn_primary.evaluate('(el) => getComputedStyle(el).transform')
            
            self.css_results['btn_primary_hover'] = {
                'background_color': hover_bg_color,
                'box_shadow': hover_box_shadow,
                'transform': hover_transform
            }
    
    async def test_consistent_icon_properties(self):
        """Test consistent icon properties"""
        print("Testing consistent icon properties...")
        
        icons = await self.page.query_selector_all('.task-icon')
        icon_measurements = []
        
        for i, icon in enumerate(icons):
            width = await icon.evaluate('(el) => getComputedStyle(el).width')
            height = await icon.evaluate('(el) => getComputedStyle(el).height')
            display = await icon.evaluate('(el) => getComputedStyle(el).display')
            align_items = await icon.evaluate('(el) => getComputedStyle(el).alignItems')
            
            icon_measurements.append({
                'index': i,
                'width': width,
                'height': height,
                'display': display,
                'align_items': align_items
            })
        
        self.css_results['task_icons'] = icon_measurements
        
        # Test status icons for consistency
        status_icons = await self.page.query_selector_all('.status-icon')
        status_measurements = []
        
        for i, icon in enumerate(status_icons):
            width = await icon.evaluate('(el) => getComputedStyle(el).width')
            height = await icon.evaluate('(el) => getComputedStyle(el).height')
            border_radius = await icon.evaluate('(el) => getComputedStyle(el).borderRadius')
            
            status_measurements.append({
                'index': i,
                'width': width,
                'height': height,
                'border_radius': border_radius
            })
        
        self.css_results['status_icons'] = status_measurements
    
    async def run_all_css_tests(self):
        """Run all CSS assertion tests for improved UI"""
        await self.setup()
        
        try:
            await self.test_task_card_properties()
            await self.test_improved_typography_properties()
            await self.test_improved_button_properties()
            await self.test_consistent_icon_properties()
            
            # Save results
            with open('../results/css_assertions_post.json', 'w') as f:
                json.dump(self.css_results, f, indent=2)
                
        finally:
            await self.teardown()
        
        return self.css_results

async def main():
    """Main CSS test execution for improved UI"""
    tester = TestImprovedCSS()
    results = await tester.run_all_css_tests()
    
    print("\n=== Improved UI CSS Test Results ===")
    for category, measurements in results.items():
        print(f"{category}: {json.dumps(measurements, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())