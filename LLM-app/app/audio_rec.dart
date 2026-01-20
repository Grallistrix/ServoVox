import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';

class AudioRecorder {
  final _recorder = AudioRecorder();

  Future<File> record10s() async {
    final dir = await getTemporaryDirectory();
    final path = '${dir.path}/input.wav';

    await _recorder.start(
      const RecordConfig(encoder: AudioEncoder.wav),
      path: path,
    );

    await Future.delayed(const Duration(seconds: 10));
    await _recorder.stop();

    return File(path);
  }
}
