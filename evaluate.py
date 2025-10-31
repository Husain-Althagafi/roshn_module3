"""
ROSHN PULSE Module 3: Comprehensive Evaluation Script
======================================================
Tests extraction performance across all sample logs and calculates metrics
"""

import sys
import glob
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from extractor import DailyLogExtractor
from schema import DailyLogExtraction


class ExtractionEvaluator:
    """Evaluates extraction performance across multiple logs"""

    def __init__(self):
        self.extractor = DailyLogExtractor()
        self.results = []
        self.errors = []

    def evaluate_all_logs(self, log_dir: str = "data/sample_logs"):
        """
        Evaluate extraction on all logs in directory

        Args:
            log_dir: Directory containing log files
        """
        log_files = sorted(glob.glob(f"{log_dir}/log_*.txt"))

        print("=" * 80)
        print("ROSHN PULSE MODULE 3 - FULL EVALUATION")
        print("=" * 80)
        print(f"\nFound {len(log_files)} log files")
        print(f"Starting evaluation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        for log_file in log_files:
            self._evaluate_single_log(log_file)

        self._print_summary()
        self._print_detailed_results()
        self._save_results()

    def _evaluate_single_log(self, log_file: str):
        """Evaluate extraction on a single log file"""
        log_name = Path(log_file).name

        try:
            # Read log
            with open(log_file, 'r', encoding='utf-8') as f:
                text = f.read()

            # Extract
            result = self.extractor.extract_from_text(text)

            # Store results
            log_result = {
                'log_name': log_name,
                'success': True,
                'metadata': {
                    'date': str(result.log_date) if result.log_date else None,
                    'site': result.site_name,
                    'manager': result.submitted_by,
                },
                'counts': {
                    'tasks': result.total_tasks_completed,
                    'blockers': result.total_blockers,
                    'incidents': result.total_incidents,
                },
                'tasks': [
                    {
                        'name': task.task_name[:80] + ('...' if len(task.task_name) > 80 else ''),
                        'location': task.location,
                        'crew': task.crew
                    }
                    for task in result.completed_tasks
                ],
                'blockers': [
                    {
                        'issue': blocker.issue[:80] + ('...' if len(blocker.issue) > 80 else ''),
                        'cause': blocker.cause
                    }
                    for blocker in result.blockers
                ],
                'incidents': [
                    {
                        'type': incident.incident_type,
                        'severity': incident.severity,
                        'description': incident.description[:80] + ('...' if len(incident.description) > 80 else '')
                    }
                    for incident in result.incidents
                ]
            }

            self.results.append(log_result)
            print(f"[OK] {log_name}: {result.total_tasks_completed}T / {result.total_blockers}B / {result.total_incidents}I")

        except Exception as e:
            error_result = {
                'log_name': log_name,
                'success': False,
                'error': str(e)
            }
            self.errors.append(error_result)
            print(f"[ERROR] {log_name}: {str(e)}")

    def _print_summary(self):
        """Print evaluation summary statistics"""
        print("\n" + "=" * 80)
        print("EVALUATION SUMMARY")
        print("=" * 80)

        total_logs = len(self.results) + len(self.errors)
        successful = len(self.results)
        failed = len(self.errors)

        print(f"\nTotal Logs Processed: {total_logs}")
        print(f"  Successful: {successful} ({successful/total_logs*100:.1f}%)")
        print(f"  Failed: {failed} ({failed/total_logs*100:.1f}%)")

        if self.results:
            # Aggregate statistics
            total_tasks = sum(r['counts']['tasks'] for r in self.results)
            total_blockers = sum(r['counts']['blockers'] for r in self.results)
            total_incidents = sum(r['counts']['incidents'] for r in self.results)

            avg_tasks = total_tasks / len(self.results)
            avg_blockers = total_blockers / len(self.results)
            avg_incidents = total_incidents / len(self.results)

            print(f"\nExtraction Statistics:")
            print(f"  Total Tasks: {total_tasks} (avg: {avg_tasks:.1f} per log)")
            print(f"  Total Blockers: {total_blockers} (avg: {avg_blockers:.1f} per log)")
            print(f"  Total Incidents: {total_incidents} (avg: {avg_incidents:.1f} per log)")

            # Metadata extraction success
            logs_with_date = sum(1 for r in self.results if r['metadata']['date'])
            logs_with_site = sum(1 for r in self.results if r['metadata']['site'])
            logs_with_manager = sum(1 for r in self.results if r['metadata']['manager'])

            print(f"\nMetadata Extraction Success Rate:")
            print(f"  Date: {logs_with_date}/{len(self.results)} ({logs_with_date/len(self.results)*100:.1f}%)")
            print(f"  Site: {logs_with_site}/{len(self.results)} ({logs_with_site/len(self.results)*100:.1f}%)")
            print(f"  Manager: {logs_with_manager}/{len(self.results)} ({logs_with_manager/len(self.results)*100:.1f}%)")

            # Location extraction
            tasks_with_location = sum(
                1 for r in self.results
                for task in r['tasks']
                if task['location']
            )
            total_task_count = sum(len(r['tasks']) for r in self.results)
            if total_task_count > 0:
                print(f"\nLocation Extraction:")
                print(f"  Tasks with location: {tasks_with_location}/{total_task_count} ({tasks_with_location/total_task_count*100:.1f}%)")

            # Blocker cause identification
            blockers_with_cause = sum(
                1 for r in self.results
                for blocker in r['blockers']
                if blocker['cause']
            )
            total_blocker_count = sum(len(r['blockers']) for r in self.results)
            if total_blocker_count > 0:
                print(f"\nBlocker Cause Identification:")
                print(f"  Blockers with cause: {blockers_with_cause}/{total_blocker_count} ({blockers_with_cause/total_blocker_count*100:.1f}%)")

            # Incident severity classification
            incidents_with_severity = sum(
                1 for r in self.results
                for incident in r['incidents']
                if incident['severity']
            )
            total_incident_count = sum(len(r['incidents']) for r in self.results)
            if total_incident_count > 0:
                print(f"\nIncident Severity Classification:")
                print(f"  Incidents with severity: {incidents_with_severity}/{total_incident_count} ({incidents_with_severity/total_incident_count*100:.1f}%)")

                # Severity breakdown
                severity_counts = defaultdict(int)
                for r in self.results:
                    for incident in r['incidents']:
                        if incident['severity']:
                            severity_counts[incident['severity']] += 1

                print(f"  Severity breakdown:")
                for severity, count in sorted(severity_counts.items()):
                    print(f"    {severity.title()}: {count}")

    def _print_detailed_results(self):
        """Print detailed results for logs with potential issues"""
        print("\n" + "=" * 80)
        print("POTENTIAL ISSUES")
        print("=" * 80)

        # Logs with no extractions at all
        empty_logs = [r for r in self.results if r['counts']['tasks'] == 0 and r['counts']['blockers'] == 0 and r['counts']['incidents'] == 0]
        if empty_logs:
            print(f"\nLogs with ZERO extractions ({len(empty_logs)}):")
            for log in empty_logs:
                print(f"  - {log['log_name']}")
        else:
            print("\n[OK] All logs have at least one extraction")

        # Logs with missing metadata
        no_metadata = [r for r in self.results if not r['metadata']['date'] or not r['metadata']['site'] or not r['metadata']['manager']]
        if no_metadata:
            print(f"\nLogs with missing metadata ({len(no_metadata)}):")
            for log in no_metadata:
                missing = []
                if not log['metadata']['date']:
                    missing.append("date")
                if not log['metadata']['site']:
                    missing.append("site")
                if not log['metadata']['manager']:
                    missing.append("manager")
                print(f"  - {log['log_name']}: missing {', '.join(missing)}")
        else:
            print("\n[OK] All logs have complete metadata")

        # Logs with unusually high extraction counts (possible over-extraction)
        high_task_logs = [r for r in self.results if r['counts']['tasks'] > 10]
        if high_task_logs:
            print(f"\nLogs with high task counts (>10) - possible over-extraction:")
            for log in high_task_logs:
                print(f"  - {log['log_name']}: {log['counts']['tasks']} tasks")

        high_incident_logs = [r for r in self.results if r['counts']['incidents'] > 3]
        if high_incident_logs:
            print(f"\nLogs with high incident counts (>3) - possible over-extraction:")
            for log in high_incident_logs:
                print(f"  - {log['log_name']}: {log['counts']['incidents']} incidents")

        # Print errors if any
        if self.errors:
            print(f"\nExtraction Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error['log_name']}: {error['error']}")

    def _save_results(self):
        """Save results to JSON file"""
        output_file = f"data/evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        results_data = {
            'evaluation_timestamp': datetime.now().isoformat(),
            'total_logs': len(self.results) + len(self.errors),
            'successful_extractions': len(self.results),
            'failed_extractions': len(self.errors),
            'results': self.results,
            'errors': self.errors
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)

        print(f"\n" + "=" * 80)
        print(f"Results saved to: {output_file}")
        print("=" * 80)


def main():
    """Main evaluation entry point"""
    evaluator = ExtractionEvaluator()
    evaluator.evaluate_all_logs()


if __name__ == "__main__":
    main()
