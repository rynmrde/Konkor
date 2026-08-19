# A2 Android Build Bootstrap QA Handoff

| Field | Value |
|---|---|
| Helper role | Android QA and build-reproducibility support |
| Branch | `parallel/help-a2-m3-android-build-bootstrap` |
| Baseline | `origin/main` at `72dc76e56b7ae625ad1904c76910eeaec5f90f58` |
| Scope | Gradle wrapper and debug-build reproducibility only |
| Main/release activity | None |

## Problem Found

The verified baseline had no Gradle wrapper and configured its `debug` build type to use `${rootDir}/debug.keystore`, although that keystore is ignored and absent from a clean checkout. As a result, `:app:assembleDebug` fails during debug signing unless a developer manually creates an untracked file. The Android plugin also requires Gradle `9.3.1` or newer, so a wrapper pinned to an earlier version cannot build this project.

## Change

This helper branch adds the standard Gradle wrapper files pinned to **Gradle 9.3.1**. It also removes the custom missing-file debug signing configuration and makes the debug build type use Android Gradle Plugin’s standard local `debug` signing configuration. The release signing configuration, application ID, namespace, min/target/compile SDK declarations, and version fields are unchanged.

| File | Change |
|---|---|
| `gradlew`, `gradlew.bat`, `gradle/wrapper/*` | Add standard wrapper, distribution URL `gradle-9.3.1-bin.zip`. |
| `app/build.gradle.kts` | Use standard debug signing configuration; retain release signing exactly as configured. |

## Validation

After deleting the ignored `debug.keystore`, this command succeeded from the project wrapper:

```text
ANDROID_HOME=/home/ubuntu/android-sdk ANDROID_SDK_ROOT=/home/ubuntu/android-sdk ./gradlew :app:assembleDebug --stacktrace
```

The resulting debug APK was produced successfully. This helper does not assert signed-release, installation, instrumentation-device, or feature-flow QA; those remain foreman gates.
