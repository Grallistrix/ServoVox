class ChatMessage {
  final String role; // user | assistant
  final String text;
  final String? audioPath;
  final DateTime time;

  ChatMessage({
    required this.role,
    required this.text,
    this.audioPath,
  }) : time = DateTime.now();
}
