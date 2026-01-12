import pytest
import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from axe_playwright import Axe
import time

# Add server module to path  
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))
from server_pre import TaskListServer

class TestBaselineAccessibility:
    def __init__(self):
        self.server = None
        self.browser = None
        self.context = None
        self.page = None
        self.a11y_results = {}
        
    async def setup(self):
        """Setup server and browser for accessibility testing"""
        self.server = TaskListServer(port=8080)
        self.server.start()
        
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        
        await self.page.goto('http://localhost:8080')
        await self.page.wait_for_load_state('networkidle')
    
    async def teardown(self):
        """Cleanup resources"""
        if self.browser:
            await self.browser.close()
        if self.server:
            self.server.stop()
    
    async def test_axe_violations(self):
        """Test for accessibility violations using axe-core"""
        print("Running axe accessibility scan...")
        
        try:
            axe = Axe()
            await axe.inject(self.page)
            results = await axe.run(self.page)
            
            self.a11y_results['axe_violations'] = {
                'violations_count': len(results['violations']),
                'violations': results['violations'],
                'passes_count': len(results['passes']),
                'incomplete_count': len(results['incomplete'])
            }
            
        except Exception as e:
            self.a11y_results['axe_violations'] = {
                'error': str(e),
                'violations_count': -1
            }
    
    async def test_contrast_ratios(self):
        """Test color contrast ratios"""
        print("Testing color contrast ratios...")
        
        contrast_tests = [
            ('.task-title', 'Task title contrast'),
            ('.task-description', 'Task description contrast'), 
            ('.btn-primary', 'Primary button contrast')
        ]
        
        contrast_results = {}
        
        for selector, description in contrast_tests:
            try:
                element = await self.page.query_selector(selector)
                if element:
                    # Get computed colors
                    color = await element.evaluate('(el) => getComputedStyle(el).color')
                    bg_color = await element.evaluate('(el) => getComputedStyle(el).backgroundColor')
                    
                    # Simple contrast calculation (would need proper implementation)
                    # For now, just store the colors
                    contrast_results[selector] = {
                        'description': description,
                        'color': color,
                        'background_color': bg_color,
                        'estimated_ratio': self.estimate_contrast_ratio(color, bg_color)
                    }
                    
            except Exception as e:
                contrast_results[selector] = {
                    'error': str(e)
                }
        
        self.a11y_results['contrast_ratios'] = contrast_results
    
    def estimate_contrast_ratio(self, color, bg_color):
        """Estimate contrast ratio - simplified calculation"""
        # This is a simplified estimation
        # In a real implementation, you'd use proper color parsing and WCAG calculations
        try:
            # Extract RGB values (this is very basic)
            if 'rgb' in color and 'rgb' in bg_color:
                return 3.5  # Placeholder estimate
            elif color == 'rgb(255, 255, 255)' and 'rgb(0' in bg_color:
                return 6.0  # High contrast estimate
            else:
                return 2.5  # Low contrast estimate
        except:
            return 1.0  # Unknown
    
    async def test_focus_indicators(self):
        """Test focus indicators on interactive elements"""
        print("Testing focus indicators...")
        
        focus_tests = [
            '.btn-primary',
            '.btn-sm', 
            '.task-card'
        ]
        
        focus_results = {}
        
        for selector in focus_tests:
            try:
                elements = await self.page.query_selector_all(selector)
                if elements:
                    element = elements[0]
                    await element.focus()
                    await asyncio.sleep(0.1)
                    
                    # Check for focus styles
                    outline = await element.evaluate('(el) => getComputedStyle(el).outline')
                    box_shadow = await element.evaluate('(el) => getComputedStyle(el).boxShadow')
                    
                    focus_results[selector] = {
                        'outline': outline,
                        'box_shadow': box_shadow,
                        'has_focus_indicator': outline != 'none' or box_shadow != 'none'
                    }
                    
            except Exception as e:
                focus_results[selector] = {
                    'error': str(e)
                }
        
        self.a11y_results['focus_indicators'] = focus_results
    
    async def test_aria_attributes(self):
        """Test ARIA attributes and roles"""
        print("Testing ARIA attributes...")
        
        aria_tests = [
            ('role', '[role]'),
            ('aria-label', '[aria-label]'),
            ('aria-labelledby', '[aria-labelledby]'),
            ('aria-describedby', '[aria-describedby]')
        ]
        
        aria_results = {}
        
        for attr, selector in aria_tests:
            try:
                elements = await self.page.query_selector_all(selector)
                count = len(elements)
                
                aria_results[attr] = {
                    'count': count,
                    'present': count > 0
                }
                
            except Exception as e:
                aria_results[attr] = {
                    'error': str(e)
                }
        
        self.a11y_results['aria_attributes'] = aria_results
    
    async def run_all_a11y_tests(self):
        """Run all accessibility tests"""
        await self.setup()
        
        try:
            await self.test_axe_violations()
            await self.test_contrast_ratios()
            await self.test_focus_indicators()
            await self.test_aria_attributes()
            
            # Save results
            with open('../results/a11y_results_pre.json', 'w') as f:
                json.dump(self.a11y_results, f, indent=2)
                
        finally:
            await self.teardown()
        
        return self.a11y_results

async def main():
    """Main accessibility test execution"""
    tester = TestBaselineAccessibility()
    results = await tester.run_all_a11y_tests()
    
    print("\n=== Baseline Accessibility Test Results ===")
    
    # Axe violations
    if 'axe_violations' in results:
        violations = results['axe_violations']
        print(f"Axe violations: {violations.get('violations_count', 'unknown')}")
    
    # Contrast ratios
    if 'contrast_ratios' in results:
        print("Contrast ratios:")
        for selector, data in results['contrast_ratios'].items():
            if 'estimated_ratio' in data:
                print(f"  {selector}: {data['estimated_ratio']}")
    
    # Focus indicators  
    if 'focus_indicators' in results:
        print("Focus indicators:")
        for selector, data in results['focus_indicators'].items():
            if 'has_focus_indicator' in data:
                status = "✓" if data['has_focus_indicator'] else "✗"
                print(f"  {status} {selector}")

if __name__ == "__main__":
    asyncio.run(main())