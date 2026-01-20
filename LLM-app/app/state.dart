late final ChatApi api;
final recorder = AudioRecorder();
final player = AudioPlayerService();

Future<void> sendText(String text) async {
  _messages.add(ChatMessage(role: 'user', text: text));
  setState(() {});

  final reply = await api.textToText(text);

  _messages.add(ChatMessage(role: 'assistant', text: reply));
  setState(() {});
}

Future<void> sendVoice() async {
  final audio = await recorder.record10s();

  _messages.add(ChatMessage(role: 'user', text: '[voice]'));
  setState(() {});

  final replyAudio = await api.audioToAudio(audio);

  _messages.add(ChatMessage(
    role: 'assistant',
    text: 'Odpowiedź głosowa',
    audioPath: replyAudio.path,
  ));
  setState(() {});
}
