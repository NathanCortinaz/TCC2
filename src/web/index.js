async function runButton() {
  await eel.run()();
  alert('Análise registrada.');
}

async function debugButton() {
  await eel.debug()();
  alert('Análise registrada.');
}

async function openResults() {
  await eel.open_results()();
}
