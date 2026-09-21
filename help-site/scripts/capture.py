#!/usr/bin/env python3
"""Run the existing capture tests on an explicitly chosen tutorial simulator.
Raw evidence is private. Import only images that have passed visual/privacy review.
"""
import argparse,datetime,json,pathlib,subprocess,os
parser=argparse.ArgumentParser()
parser.add_argument('--checkout',type=pathlib.Path,required=True)
parser.add_argument('--simulator',required=True)
parser.add_argument('--locale',choices=['en','zh-Hans'],required=True)
parser.add_argument('--output',type=pathlib.Path,required=True)
parser.add_argument('--derived-data',type=pathlib.Path,required=True)
parser.add_argument('--build',action='store_true')
parser.add_argument('--test',action='append',choices=['testCaptureWorkspaceAndSettings', 'testCaptureEnvironment', 'testCaptureProviderConfiguration', 'testCaptureNotebookResult', 'testValidateHuggingFaceAuthorization', 'testCaptureFeedback', 'testCaptureMemorySkillsAndContext', 'testCaptureAccountAndRestore', 'testCaptureAgentReasoning', 'testCaptureGallery', 'testCaptureCloneForm', 'testCaptureShell', 'testCaptureRichCells', 'testCapturePackageImportAndTable', 'testCaptureEnvironmentVariable', 'testCaptureRemoteForms', 'testCaptureRelaunchApp', 'testCaptureGitHubSignIn', 'testCaptureSSHPasswordAndKey', 'testCaptureExportMenu', 'testCapturePackageCatalog', 'testCaptureCodexCatalog', 'testCaptureActualClone', 'testCaptureGitCommitPushAndPR', 'testCaptureEditingTools', 'testCaptureCompatiblePackageInstall', 'testCaptureConnectedGitHub', 'testCaptureDownloadLocation', 'testCaptureAgentConfirmation'])
args=parser.parse_args()
root=pathlib.Path(__file__).resolve().parents[1]
output=args.output.expanduser().resolve()
if output.is_relative_to(root.parent):parser.error('Raw output must be outside the website checkout.')
devices=json.loads(subprocess.check_output(['xcrun','simctl','list','devices','--json'],text=True))['devices']
device=next((d for group in devices.values() for d in group if d['udid']==args.simulator),None)
if not device or not device['name'].startswith('Vibeit Tutorials '):parser.error('Use a dedicated Vibeit Tutorials simulator.')
if device['state']!='Booted':parser.error('Boot the dedicated simulator before capture.')
checkout=args.checkout.expanduser().resolve()
if not (checkout/'App/UITests/HelpScreenshotCaptureUITests.swift').is_file():parser.error('Capture tests are missing from the isolated App checkout.')
output.mkdir(parents=True,exist_ok=True)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
run=output/f'{stamp}-{args.locale}'
run.mkdir(mode=0o700)
base=['xcodebuild','-project',str(checkout/'App/PyDev.xcodeproj'),'-scheme','VibeitHelpCapture','-configuration','Release','-destination',f'platform=iOS Simulator,id={args.simulator}','-derivedDataPath',str(args.derived_data.expanduser().resolve())]
if args.build:
 with open(run/'build.log','w') as log:
  subprocess.run(base+['-skipMacroValidation','COMPILER_INDEX_STORE_ENABLE=NO','ONLY_ACTIVE_ARCH=YES','OTHER_SWIFT_FLAGS=$(inherited) -DVIBEIT_HELP_CAPTURE','build-for-testing'],cwd=checkout,stdout=log,stderr=subprocess.STDOUT,check=True)
tests=args.test or ['testCaptureWorkspaceAndSettings','testCaptureEnvironment','testCaptureFeedback','testCaptureNotebookResult','testCaptureProviderConfiguration']
result=run/'capture.xcresult'
command=base+['-parallel-testing-enabled','NO','-collect-test-diagnostics','never','-resultBundlePath',str(result)]
command += [f'-only-testing:PyDev_iOSUITests/HelpScreenshotCaptureUITests/{name}' for name in tests]
command += ['test-without-building']
env={**os.environ,'TEST_RUNNER_HELP_CAPTURE_LOCALE':args.locale}
with open(run/'test.log','w') as log:completed=subprocess.run(command,cwd=checkout,env=env,stdout=log,stderr=subprocess.STDOUT)
if result.exists():subprocess.run(['xcrun','xcresulttool','export','attachments','--path',str(result),'--output-path',str(run/'attachments')],check=True,stdout=subprocess.DEVNULL)
print(f'Private capture output: {run}')
print('Visual review is required even when tests pass. No screenshot has been published.')
raise SystemExit(completed.returncode)
