async function adicionarArquivo() {
  listaArquivos = await eel.novo_arquivo()();
  await atualizaLista(listaArquivos);
  alert('Arquivo adicionado!');
}

async function excluirArquivo() {
  numArquivo = prompt('Digite o número do arquivo que deseja remover:');
  if (numArquivo === null) excluirArquivo();
  else resultado = await eel.remove_arquivo(numArquivo)();
  console.log(resultado);
  if (resultado == true) {
    listaArquivos = await eel.atualiza_lista_arquivos()();
    atualizaLista(listaArquivos);
    alert('Arquivo removido!');
  } else alert('Arquivo não encontrado!');
}

async function definirEmail() {
  email = prompt('Digite um endereço de e-mail para receber os alertas:');
  if (email === null) definirEmail();
  else await eel.atualizaDestinatario(email);
  alert(`Email definido como "${email}"`);
}

async function atualizaLista(arquivosRecebidos) {
  document.getElementById('arquivosMonitorados').innerHTML = '';
  console.log(arquivosRecebidos);
  if (Object.keys(arquivosRecebidos).length == 0) {
    document.getElementById('arquivosMonitorados').innerHTML = 'Clique em "Adicionar arquivo" para monitorá-lo';
  } else {
    for (item in arquivosRecebidos) {
      document.getElementById('arquivosMonitorados').innerHTML +=
        '<li>[' + item + '] ' + arquivosRecebidos[item] + '</li>';
    }
  }
}

async function verificaModificacoes() {
  definirEmail();
  eel.rotina_verifica_alteracoes()();
}
