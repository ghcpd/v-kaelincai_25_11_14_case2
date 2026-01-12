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
from server_pre import TaskListServer

class TestBaselineVisual:
    def __init__(self):
        self.server = None
        self.browser = None
        self.context = None
        self.page = None
        self.results = {}
        
    async def setup(self):
        """Setup server and browser for testing"""
        # Start the baseline server
        self.server = TaskListServer(port=8080)
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
        print(f"Running test case: {test_id}")
        
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
            await self.page.goto(step['url'])
            await self.page.wait_for_load_state('networkidle')
            
        elif action == 'wait':
            await asyncio.sleep(step['duration'] / 1000)
            
        elif action == 'screenshot':
            screenshot_path = f"../screenshots/{step['name']}"
            await self.page.screenshot(path=screenshot_path, full_page=True)
            result['screenshots'].append(screenshot_path)
            
        elif action == 'locate':
            element = await self.page.query_selector(step['selector'])
            if not element:
                raise Exception(f"Element not found: {step['selector']}")
                
        elif action == 'get_computed_style':
            selector = step.get('selector') or result.get('last_selector')
            if not selector:
                raise Exception("No selector available for get_computed_style")
                
            element = await self.page.query_selector(selector)
            if element:
                for prop in step['properties']:
                    value = await element.evaluate(f'(el) => getComputedStyle(el).{prop.replace("-", "")}')
                    result['measurements'][f'{selector}_{prop}'] = value
                    
        elif action == 'hover':
            await self.page.hover(step['selector'])
            
        elif action == 'focus':
            await self.page.focus(step['selector'])
    
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
        with open('../results/results_pre.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return self.results

async def main():
    """Main test execution function"""
    tester = TestBaselineVisual()
    results = await tester.run_all_tests()
    
    # Generate summary
    passed = sum(1 for r in results.values() if r['status'] == 'passed')
    total = len(results)
    
    print(f"\n=== Baseline UI Test Results ===")
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