import pytest
import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright, Browser, Page
from PIL import Image
import time

# Add server module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))
from server_post import TaskListImprovedServer

class TestImprovedVisual:
    def __init__(self):
        self.server = None
        self.browser = None
        self.context = None
        self.page = None
        self.results = {}
        
    async def setup(self):
        """Setup server and browser for testing"""
        # Start the improved server
        self.server = TaskListImprovedServer(port=8081)
        self.server.start()
        
        # Setup Playwright
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            device_scale_factor=1
        )
        self.page = await self.context.new_page()
        
        # Load test data
        with open('../../test_data.json', 'r') as f:
            self.test_data = json.load(f)
    
    async def teardown(self):
        """Cleanup resources"""
        if self.browser:
            await self.browser.close()
        if self.server:
            self.server.stop()
    
    async def run_test_case(self, test_case):
        """Execute a single test case"""
        test_id = test_case['test_id']
        print(f"Running improved UI test case: {test_id}")
        
        result = {
            'test_id': test_id,
            'description': test_case['description'],
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'running',
            'measurements': {},
            'screenshots': [],
            'errors': []
        }
        
        try:
            for step in test_case['steps']:
                await self.execute_step(step, result)
            
            # Validate improvements
            await self.validate_improvements(test_case, result)
            
            result['status'] = 'passed'
            
        except Exception as e:
            result['status'] = 'failed'
            result['errors'].append(str(e))
            print(f"Test {test_id} failed: {e}")
        
        return result
    
    async def execute_step(self, step, result):
        """Execute a single test step"""
        action = step['action']
        
        if action == 'navigate':
            # Use improved UI URL
            url = step['url'].replace('8080', '8081')
            await self.page.goto(url)
            await self.page.wait_for_load_state('networkidle')
            
        elif action == 'wait':
            await asyncio.sleep(step['duration'] / 1000)
            
        elif action == 'screenshot':
            # Update screenshot names for improved UI
            screenshot_name = step['name'].replace('pre_', 'post_')
            screenshot_path = f"../screenshots/{screenshot_name}"
            await self.page.screenshot(path=screenshot_path, full_page=True)
            result['screenshots'].append(screenshot_path)
            
        elif action == 'locate':
            element = await self.page.query_selector(step['selector'])
            if not element:
                raise Exception(f"Element not found: {step['selector']}")
            result['last_selector'] = step['selector']
                
        elif action == 'get_computed_style':
            selector = step.get('selector') or result.get('last_selector')
            if not selector:
                raise Exception("No selector available for get_computed_style")
                
            element = await self.page.query_selector(selector)
            if element:
                for prop in step['properties']:
                    css_prop = prop.replace('-', '')
                    if css_prop == 'fontweight':
                        css_prop = 'fontWeight'
                    elif css_prop == 'fontsize':
                        css_prop = 'fontSize'
                    elif css_prop == 'lineheight':
                        css_prop = 'lineHeight'
                    elif css_prop == 'backgroundcolor':
                        css_prop = 'backgroundColor'
                    elif css_prop == 'borderradius':
                        css_prop = 'borderRadius'
                    elif css_prop == 'boxshadow':
                        css_prop = 'boxShadow'
                    elif css_prop == 'verticalalign':
                        css_prop = 'verticalAlign'
                        
                    value = await element.evaluate(f'(el) => getComputedStyle(el).{css_prop}')
                    result['measurements'][f'{selector}_{prop}'] = value
                    
        elif action == 'hover':
            await self.page.hover(step['selector'])
            
        elif action == 'focus':
            await self.page.focus(step['selector'])
    
    async def validate_improvements(self, test_case, result):
        """Validate that improvements meet acceptance criteria"""
        expected = test_case.get('expected', {})
        measurements = result['measurements']
        
        # Load expected values for improved UI
        with open('../data/expected_post.json', 'r') as f:
            expected_post = json.load(f)
        
        # Validate specific improvements based on test case
        test_id = test_case['test_id']
        
        if test_id == 'card_spacing_hierarchy':
            # Check padding improvement
            card_padding = measurements.get('.task-card_padding', '')
            if '20px' not in card_padding:
                result['errors'].append(f"Card padding not improved: {card_padding}")
            
            # Check font size improvement
            title_font_size = measurements.get('.task-card .task-title_font-size', '')
            if title_font_size and float(title_font_size.replace('px', '')) < 16:
                result['errors'].append(f"Title font size not improved: {title_font_size}")
                
        elif test_id == 'button_consistency_hover':
            # Check button background color
            btn_bg = measurements.get('.btn-primary_background-color', '')
            if 'rgb(13, 71, 161)' not in btn_bg and '#0D47A1' not in btn_bg:
                result['errors'].append(f"Button color not improved: {btn_bg}")
    
    async def run_all_tests(self):
        """Run all test cases from test_data.json"""
        await self.setup()
        
        try:
            for test_case in self.test_data['test_cases']:
                result = await self.run_test_case(test_case)
                self.results[test_case['test_id']] = result
                
        finally:
            await self.teardown()
        
        # Save results
        with open('../results/results_post.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return self.results

async def main():
    """Main test execution function"""
    tester = TestImprovedVisual()
    results = await tester.run_all_tests()
    
    # Generate summary
    passed = sum(1 for r in results.values() if r['status'] == 'passed')
    total = len(results)
    
    print(f"\n=== Improved UI Test Results ===")
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    for test_id, result in results.items():
        status_icon = "✓" if result['status'] == 'passed' else "✗"
        print(f"{status_icon} {test_id}: {result['status']}")
        if result['errors']:
            for error in result['errors']:
                print(f"    Error: {error}")

if __name__ == "__main__":
    asyncio.run(main())