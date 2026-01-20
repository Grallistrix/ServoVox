import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ChatApi {
  final String baseUrl;
  ChatApi(this.baseUrl);

  Future<String> textToText(String text) async {
    final res = await http.post(
      Uri.parse('$baseUrl/text_to_text'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'text': text}),
    );

    final data = jsonDecode(res.body);
    return data['text'];
  }

  Future<String> audioToText(File file) async {
    final req = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/audio_to_text'),
    );

    req.files.add(await http.MultipartFile.fromPath('file', file.path));
    final res = await req.send();
    final body = await res.stream.bytesToString();

    return jsonDecode(body)['recognized_text'];
  }

  Future<File> audioToAudio(File file) async {
    final req = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/audio_to_audio'),
    );

    req.files.add(await http.MultipartFile.fromPath('file', file.path));
    final res = await req.send();

    final bytes = await res.stream.toBytes();
    final out = File('${file.parent.path}/reply_${DateTime.now().millisecondsSinceEpoch}.wav');
    await out.writeAsBytes(bytes);

    return out;
  }
}
