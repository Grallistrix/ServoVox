import 'dart:async';
import 'package:flutter/material.dart';

void main() {
  runApp(const ChatApp());
}

const bool testing = true;

class ChatApp extends StatelessWidget {
  const ChatApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ServoVOX',
      theme: ThemeData.dark(useMaterial3: true),
      home: const ChatPage(),
    );
  }
}

class ChatMessage {
  final String role; // user | assistant
  final String text;
  final DateTime time;

  ChatMessage(this.role, this.text) : time = DateTime.now();
}

class ChatResponse {
  final String text;
  final List<int>? audioBytes; // placeholder pod audio

  ChatResponse({required this.text, this.audioBytes});
}

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final List<ChatMessage> _messages = [];
  final TextEditingController _apiController = TextEditingController(
    text: 'http://192.168.0.10:8000',
  );
  final TextEditingController _inputController = TextEditingController();

  bool _sending = false;

  Future<ChatResponse> sendMessage({
    required String apiUrl,
    String? text,
    String? audioPath,
  }) async {
    if (testing) {
      await Future.delayed(const Duration(milliseconds: 600));
      return ChatResponse(
        text: 'TEST ODPOWIEDŹ: otrzymałem "${text ?? '[audio]'}"',
        audioBytes: null,
      );
    }

    // TU docelowo:
    // - HTTP POST
    // - multipart dla audio
    // - response: text + audio
    throw UnimplementedError();
  }

  Future<void> _onSend() async {
    final text = _inputController.text.trim();
    if (text.isEmpty || _sending) return;

    setState(() {
      _sending = true;
      _messages.add(ChatMessage('user', text));
      _inputController.clear();
    });

    final response = await sendMessage(apiUrl: _apiController.text, text: text);

    setState(() {
      _messages.add(ChatMessage('assistant', response.text));
      _sending = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('LLM Chat')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8),
            child: TextField(
              controller: _apiController,
              decoration: const InputDecoration(
                labelText: 'API address',
                border: OutlineInputBorder(),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(8),
              itemCount: _messages.length,
              itemBuilder: (context, i) {
                final m = _messages[i];
                final isUser = m.role == 'user';
                return Align(
                  alignment: isUser
                      ? Alignment.centerRight
                      : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    padding: const EdgeInsets.all(10),
                    constraints: BoxConstraints(
                      maxWidth: MediaQuery.of(context).size.width * 0.75,
                    ),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.blueAccent : Colors.grey.shade800,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(m.text),
                  ),
                );
              },
            ),
          ),
          SafeArea(
            child: Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.mic),
                  onPressed: () {
                    // placeholder pod nagrywanie audio
                  },
                ),
                Expanded(
                  child: TextField(
                    controller: _inputController,
                    decoration: const InputDecoration(
                      hintText: 'Wpisz wiadomość',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _onSend(),
                  ),
                ),
                IconButton(
                  icon: _sending
                      ? const CircularProgressIndicator()
                      : const Icon(Icons.send),
                  onPressed: _sending ? null : _onSend,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
