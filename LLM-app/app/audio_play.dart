import 'package:just_audio/just_audio.dart';

class AudioPlayerService {
  final _player = AudioPlayer();

  Future<void> play(String path) async {
    await _player.setFilePath(path);
    await _player.play();
  }
}
