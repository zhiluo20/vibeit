# 1.0.1 environment restart behavior

Actual UI verification saved `VIBEIT_DEMO=tutorial` in Settings → Environment. The value is present in the app preference store. A notebook run after the visible Restart action printed `VIBEIT_DEMO = None`.

Source: `App/iOS/InProcessPyKernel.swift` assembles and applies `KernelStartupEnvironment.build()` only in `start()`. Its `restart()` resets the Python namespace and counter while retaining the interpreter. It does not rebuild or synchronize `os.environ`.

The earlier HF check proved that the token works after an App launch followed by a kernel restart; it did not prove that a token changed during an already-running interpreter is applied by that restart alone. Tutorial wording must distinguish those cases.

Workaround under verification: completely close and reopen Vibeit after changing startup environment variables. Do not insert `os.environ` assignments into the verification notebook to make the example pass. App behavior remains unchanged in this documentation task.
