#!/usr/bin/env python3
"""
Quick Testing Protocol - Immediate kernel validation
Tests current architect-kernel against existing issue queue
"""

import subprocess
import json
import time
from datetime import datetime

class KernelTester:
    def __init__(self):
        self.test_start = datetime.now()
        self.results = {}
    
    def get_issue_queue(self):
        """Get current GitHub issues for testing"""
        try:
            result = subprocess.run(
                ['gh', 'issue', 'list', '--json', 'number,title,labels,state'],
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"❌ GitHub integration failed: {e}")
            return []
    
    def analyze_queue(self, issues):
        """Analyze issue queue for testing potential"""
        if not issues:
            return {"error": "No issues found for testing"}
        
        analysis = {
            "total_issues": len(issues),
            "priorities": {},
            "types": {},
            "testable": 0
        }
        
        for issue in issues:
            # Count by labels (approximate priorities)
            labels = [label.get('name', '') for label in issue.get('labels', [])]
            
            for label in labels:
                if label.startswith('p'):
                    analysis["priorities"][label] = analysis["priorities"].get(label, 0) + 1
                analysis["types"][label] = analysis["types"].get(label, 0) + 1
            
            # Count testable issues (have clear deliverables)
            if any(keyword in issue['title'].lower() for keyword in 
                   ['implement', 'create', 'add', 'build', 'design']):
                analysis["testable"] += 1
        
        return analysis
    
    def test_kernel_readiness(self):
        """Test if kernel repository is ready for testing"""
        checks = {
            "readme_exists": False,
            "frameworks_dir": False,
            "specializations_dir": False,
            "framework_files": 0,
            "specialization_files": 0,
            "testing_dir": False
        }
        
        import os
        
        # Check README
        checks["readme_exists"] = os.path.exists("README.md")
        
        # Check directories
        checks["frameworks_dir"] = os.path.exists("frameworks/")
        checks["specializations_dir"] = os.path.exists("specializations/")  
        checks["testing_dir"] = os.path.exists("testing/")
        
        # Count framework files
        if os.path.exists("frameworks/"):
            checks["framework_files"] = len([f for f in os.listdir("frameworks/") if f.endswith('.md')])
        
        # Count specialization files  
        if os.path.exists("specializations/"):
            checks["specialization_files"] = len([f for f in os.listdir("specializations/") if f.endswith('.md')])
        
        return checks
    
    def generate_test_report(self):
        """Generate comprehensive test readiness report"""
        print("🧪 KERNEL TESTING READINESS ASSESSMENT")
        print("=" * 50)
        
        # Test repository readiness
        print("\n📁 Repository Structure:")
        readiness = self.test_kernel_readiness()
        for check, result in readiness.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check}: {result}")
        
        # Test issue queue
        print("\n📋 Issue Queue Analysis:")
        issues = self.get_issue_queue()
        analysis = self.analyze_queue(issues)
        
        if "error" in analysis:
            print(f"  ❌ {analysis['error']}")
        else:
            print(f"  📊 Total Issues: {analysis['total_issues']}")
            print(f"  🎯 Testable Issues: {analysis['testable']}")
            print(f"  📈 Priorities: {analysis['priorities']}")
            
        # Test GitHub integration
        print("\n🔗 GitHub Integration:")
        github_works = len(issues) > 0
        print(f"  {'✅' if github_works else '❌'} GitHub CLI Access: {github_works}")
        
        # Overall assessment
        print("\n🎯 TESTING READINESS:")
        ready_for_testing = (
            readiness["readme_exists"] and 
            readiness["framework_files"] > 0 and 
            analysis.get("total_issues", 0) > 0 and
            github_works
        )
        
        print(f"  {'✅' if ready_for_testing else '❌'} Ready for Kernel Testing: {ready_for_testing}")
        
        # Identified concerns
        print("\n⚠️  TESTING CONCERNS:")
        concerns = []
        
        if readiness["framework_files"] == 0:
            concerns.append("No framework files available for loading")
        
        if not github_works:
            concerns.append("GitHub integration not functional")
            
        if analysis.get("testable", 0) == 0:
            concerns.append("No clearly testable issues in queue")
        
        # Critical concern: framework loading mechanism
        concerns.append("Framework loading mechanism not implemented (Issue #4)")
        concerns.append("LLM dynamic file loading not technically possible")
        
        for concern in concerns:
            print(f"  ⚠️  {concern}")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("  1. Implement framework loading workaround before testing")  
        print("  2. Test with human-assisted framework content delivery")
        print("  3. Validate GitHub integration in test environment")
        print("  4. Start with simple issue resolution testing")
        
        return {
            "ready": ready_for_testing,
            "issues_available": analysis.get("total_issues", 0),
            "concerns": concerns,
            "timestamp": self.test_start.isoformat()
        }

if __name__ == "__main__":
    tester = KernelTester()
    report = tester.generate_test_report()
    
    print(f"\n⏱️  Assessment completed in: {datetime.now() - tester.test_start}")
    
    if report["ready"]:
        print("\n🚀 KERNEL READY FOR TESTING!")
    else:
        print("\n🔧 KERNEL NEEDS PREPARATION BEFORE TESTING")