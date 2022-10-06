async function debugButton() {
  await eel.debug()();
  alert('Debugando...');
}

async function openResults() {
  await eel.open_results()();
}
