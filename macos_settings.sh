#!/bin/bash
# =============================================================================
# macOS System Settings Configuration Script
# Usage:
#   bash macos_settings.sh            — apply all settings
#   bash macos_settings.sh --dry-run  — preview current values, no changes made
# =============================================================================

DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "🔍 DRY RUN — showing current values only, no changes will be made."
else
  echo "🍎 Applying macOS settings..."
fi
echo ""

# Helper: print current value of a defaults key
current() {
  local domain="$1"
  local key="$2"
  local val
  val=$(defaults read "$domain" "$key" 2>/dev/null)
  if [[ -z "$val" ]]; then
    echo "(not set)"
  else
    echo "$val"
  fi
}

# Helper: run a command or skip it in dry-run mode
apply() {
  if $DRY_RUN; then
    return
  fi
  eval "$@"
}

# ─── Appearance ───────────────────────────────────────────────────────────────
echo "[ System Appearance — Dark Mode ]"
echo "  Current : $(current NSGlobalDomain AppleInterfaceStyle)"
apply defaults write NSGlobalDomain AppleInterfaceStyle Dark
$DRY_RUN || echo "  Updated → Dark"
echo ""

echo "[ Icon & Widget Style — Dark ]"
echo "  Current : $(current com.apple.WindowManager AppearanceThemeColorIndex)"
apply defaults write com.apple.WindowManager AppearanceThemeColorIndex -int 2 2>/dev/null || true
$DRY_RUN || echo "  Updated → 2 (Dark)"
echo ""

# ─── Dock ─────────────────────────────────────────────────────────────────────
echo "[ Dock — Auto-hide ]"
echo "  Current : $(current com.apple.dock autohide)"
apply defaults write com.apple.dock autohide -bool true
$DRY_RUN || echo "  Updated → true (1)"
echo ""

echo "[ Hot Corners — Disable All ]"
for pos in tl tr bl br; do
  echo "  Current wvous-${pos}-corner   : $(current com.apple.dock wvous-${pos}-corner)"
  echo "  Current wvous-${pos}-modifier : $(current com.apple.dock wvous-${pos}-modifier)"
  apply defaults write com.apple.dock wvous-${pos}-corner   -int 1
  apply defaults write com.apple.dock wvous-${pos}-modifier -int 0
done
$DRY_RUN || echo "  Updated → all corners disabled (1), modifiers cleared (0)"
echo ""

# ─── Scrolling ────────────────────────────────────────────────────────────────
echo "[ Natural Scrolling — Disabled ]"
echo "  Current : $(current NSGlobalDomain com.apple.swipescrolldirection)"
apply defaults write NSGlobalDomain com.apple.swipescrolldirection -bool false
$DRY_RUN || echo "  Updated → false (natural scrolling off) (0)"
echo ""

# ─── Tapping ──────────────────────────────────────────────────────────────────
echo "[ Tap to click — Enabled ]"
echo "  Current Apple Multitouch : $(current Clicking com.apple.AppleMultitouchTrackpad)"
echo "  Current Apple Bluetooth Multitouch : $(current Clicking com.apple.driver.AppleBluetoothMultitouch.trackpad)"
apply defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true
apply defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true
# Restart trackpad service to apply
echo "  Restarting trackpad service..."
apply defaults write NSGlobalDomain com.apple.mouse.tapBehavior -int 1
$DRY_RUN || echo "  Updated → true (tap to click on) (true)"
echo ""

# ─── Clock ────────────────────────────────────────────────────────────────────
echo "[ Clock — Show Seconds ]"
echo "  Current ShowSeconds : $(current com.apple.menuextra.clock ShowSeconds)"
echo "  Current DateFormat  : $(current com.apple.menuextra.clock DateFormat)"
apply defaults write com.apple.menuextra.clock ShowSeconds -bool true
apply defaults write com.apple.menuextra.clock DateFormat  -string "h:mm:ss"
$DRY_RUN || echo "  Updated → ShowSeconds=true, DateFormat=h:mm:ss"
echo ""

# ─── Menu Bar ─────────────────────────────────────────────────────────────────
echo "[ Menu Bar — Bluetooth Visible ]"
echo "  Current : $(defaults -currentHost read com.apple.controlcenter.plist Bluetooth)"
defaults write ~/Library/Preferences/ByHost/com.apple.controlcenter.plist Bluetooth -int 18
$DRY_RUN || echo "  Updated → true (18)"
echo ""

# This does not work in Ventura
# echo "[ Menu Bar — Volume Visible ]"
# echo "  Current : $(current com.apple.controlcenter "NSStatusItem Visible Sound")"
# apply defaults write com.apple.controlcenter '"NSStatusItem Visible Sound"' -bool true
# $DRY_RUN || echo "  Updated → true"
# echo ""

# This does not work in Ventura
# echo "[ Menu Bar — Battery Visible + Show Percentage ]"
# echo "  Current Battery Visible : $(current com.apple.controlcenter "NSStatusItem Visible Battery")"
# echo "  Current ShowPercent     : $(current com.apple.controlcenter ShowPercent)"
# apply defaults write com.apple.controlcenter '"NSStatusItem Visible Battery"' -bool true
# apply defaults write com.apple.controlcenter ShowPercent -string "1"
# $DRY_RUN || echo "  Updated → Visible=true, ShowPercent=1"
# echo ""

# ─── Tracking Speeds ──────────────────────────────────────────────────────────
echo "[ Trackpad Tracking Speed — Maximum (3.0) ]"
echo "  Current : $(current NSGlobalDomain com.apple.trackpad.scaling)"
apply defaults write NSGlobalDomain com.apple.trackpad.scaling -float 3.0
$DRY_RUN || echo "  Updated → 3.0"
echo ""

echo "[ Mouse Tracking Speed — Maximum (3.0) ]"
echo "  Current : $(current NSGlobalDomain com.apple.mouse.scaling)"
apply defaults write NSGlobalDomain com.apple.mouse.scaling -float 3.0
$DRY_RUN || echo "  Updated → 3.0"
echo ""

# ─── Restart services (only when applying) ────────────────────────────────────
if ! $DRY_RUN; then
  echo "→ Restarting Dock, SystemUIServer, and ControlCenter..."
  killall Dock           2>/dev/null || true
  killall SystemUIServer 2>/dev/null || true
  killall ControlCenter  2>/dev/null || true
  echo ""
  echo "✅ All done!"
  echo ""
  echo "⚠️  Notes:"
  echo "   • Dark mode & scrolling changes take full effect after logging out and back in."
  echo "   • If battery % doesn't appear immediately, toggle it off/on once in System Settings > Control Center."
  echo "   • Tracking speed is applied system-wide; external mice may need their own driver settings."
else
  echo "🔍 Dry run complete — no changes were made."
fi
