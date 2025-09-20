"""
Conversion service for handling file conversions.
Supports image, audio, and video conversion using appropriate libraries.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, Optional

from PIL import Image
import ffmpeg

from models.file_info import FileInfo, FileType
from models.conversion_options import ConversionOptions, ImageConversionOptions


class ConversionService:
    """Service for handling file conversions."""
    
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
    
    def _find_ffmpeg(self) -> str:
        """Find FFmpeg executable path."""
        # Check if ffmpeg is in PATH
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return 'ffmpeg'
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Check for bundled ffmpeg.exe
        possible_paths = [
            'ffmpeg.exe',
            'bin/ffmpeg.exe',
            'resources/ffmpeg.exe'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        raise RuntimeError("FFmpeg not found. Please ensure ffmpeg.exe is available.")
    
    def convert_file(
        self,
        file_info: FileInfo,
        options: ConversionOptions,
        output_path: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> bool:
        """
        Convert file based on type and options.
        
        Args:
            file_info: File information
            options: Conversion options
            output_path: Output file path
            progress_callback: Optional progress callback (0-100)
        
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            if file_info.file_type == FileType.IMAGE:
                return self._convert_image(file_info, options.image_options, output_path)
            elif file_info.file_type == FileType.AUDIO:
                return self._convert_audio(file_info, options.audio_options, output_path, progress_callback)
            elif file_info.file_type == FileType.VIDEO:
                return self._convert_video(file_info, options.video_options, output_path, progress_callback)
            else:
                return False
        except Exception as e:
            print(f"Conversion error: {e}")
            return False
    
    def _convert_image(
        self,
        file_info: FileInfo,
        options: ImageConversionOptions,
        output_path: str
    ) -> bool:
        """Convert image file."""
        try:
            with Image.open(file_info.file_path) as img:
                # Convert to RGB if necessary for JPEG
                if options.output_format.value == 'jpg' and img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if requested
                if options.resize_enabled and options.max_width and options.max_height:
                    img.thumbnail((options.max_width, options.max_height), Image.Resampling.LANCZOS)
                
                # Optimize for size if requested
                if options.size_limit_enabled and options.max_size_kb:
                    # Check if we need optimization
                    temp_path = output_path + '.check'
                    format_name = 'JPEG' if options.output_format.value.upper() == 'JPG' else options.output_format.value.upper()
                    img.save(temp_path, format=format_name)
                    current_size = os.path.getsize(temp_path)
                    os.remove(temp_path)
                    
                    max_size_bytes = options.max_size_kb * 1024
                    if current_size <= max_size_bytes:
                        # File is already small enough, just save normally
                        img.save(output_path, format=format_name)
                    else:
                        # Need optimization
                        output_path = self._optimize_image_size(img, output_path, options)
                else:
                    # Save with appropriate format
                    format_name = 'JPEG' if options.output_format.value.upper() == 'JPG' else options.output_format.value.upper()
                    img.save(output_path, format=format_name)
                
                return True
        except Exception as e:
            print(f"Image conversion error: {e}")
            return False
    
    def _optimize_image_size(self, img: Image.Image, output_path: str, options: ImageConversionOptions) -> str:
        """Optimize image to meet size requirements."""
        max_size_bytes = options.max_size_kb * 1024
        format_name = 'JPEG' if options.output_format.value.upper() == 'JPG' else options.output_format.value.upper()
        
        print(f"Target size: {max_size_bytes} bytes ({options.max_size_kb} KB)")
        
        # Try different quality levels for JPEG
        if format_name == 'JPEG':
            # Try quality levels from 95% down to 5%
            for quality in range(95, 4, -5):
                temp_path = output_path + '.tmp'
                try:
                    img.save(temp_path, format=format_name, quality=quality, optimize=True)
                    file_size = os.path.getsize(temp_path)
                    print(f"Quality {quality}%: {file_size} bytes")
                    
                    if file_size <= max_size_bytes:
                        os.replace(temp_path, output_path)
                        print(f"Success! Final size: {file_size} bytes")
                        return output_path
                    else:
                        os.remove(temp_path)
                except Exception as e:
                    print(f"Error with quality {quality}: {e}")
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            
            # If still too large, try aggressive resizing
            return self._aggressive_resize_for_size(img, output_path, max_size_bytes, format_name)
        else:
            # For PNG, try different compression levels (0-9, where 9 is maximum compression)
            for compress_level in range(9, -1, -1):
                temp_path = output_path + '.tmp'
                try:
                    img.save(temp_path, format=format_name, compress_level=compress_level, optimize=True)
                    file_size = os.path.getsize(temp_path)
                    print(f"Compression level {compress_level}: {file_size} bytes")
                    
                    if file_size <= max_size_bytes:
                        os.replace(temp_path, output_path)
                        print(f"Success! Final size: {file_size} bytes")
                        return output_path
                    else:
                        os.remove(temp_path)
                except Exception as e:
                    print(f"Error with compression {compress_level}: {e}")
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            
            # If still too large, try aggressive resizing
            return self._aggressive_resize_for_size(img, output_path, max_size_bytes, format_name)
    
    def _aggressive_resize_for_size(self, img: Image.Image, output_path: str, max_size_bytes: int, format_name: str) -> str:
        """Aggressively resize image to meet size requirements."""
        print("Trying aggressive resizing...")
        
        # Start with 50% of original size and work down
        for scale in [0.5, 0.3, 0.2, 0.1, 0.05]:
            new_size = (int(img.width * scale), int(img.height * scale))
            if new_size[0] < 10 or new_size[1] < 10:
                break
                
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            if format_name == 'JPEG':
                # Try different quality levels with resized image
                for quality in range(85, 4, -10):
                    temp_path = output_path + '.tmp'
                    try:
                        resized_img.save(temp_path, format=format_name, quality=quality, optimize=True)
                        file_size = os.path.getsize(temp_path)
                        print(f"Scale {scale}, Quality {quality}%: {file_size} bytes")
                        
                        if file_size <= max_size_bytes:
                            os.replace(temp_path, output_path)
                            print(f"Success with resizing! Final size: {file_size} bytes")
                            return output_path
                        else:
                            os.remove(temp_path)
                    except Exception as e:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
            else:
                # For PNG, try different compression levels with resized image
                for compress_level in range(9, -1, -2):
                    temp_path = output_path + '.tmp'
                    try:
                        resized_img.save(temp_path, format=format_name, compress_level=compress_level, optimize=True)
                        file_size = os.path.getsize(temp_path)
                        print(f"Scale {scale}, Compression {compress_level}: {file_size} bytes")
                        
                        if file_size <= max_size_bytes:
                            os.replace(temp_path, output_path)
                            print(f"Success with resizing! Final size: {file_size} bytes")
                            return output_path
                        else:
                            os.remove(temp_path)
                    except Exception as e:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
        
        # If we still can't meet the requirement, save with minimum settings
        print("Could not meet size requirement, saving with minimum settings")
        if format_name == 'JPEG':
            img.save(output_path, format=format_name, quality=5, optimize=True)
        else:
            img.save(output_path, format=format_name, compress_level=9, optimize=True)
        return output_path
    
    def _convert_audio(
        self,
        file_info: FileInfo,
        options,
        output_path: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> bool:
        """Convert audio file to MP3."""
        try:
            # Create FFmpeg input stream
            input_stream = ffmpeg.input(str(file_info.file_path))
            
            # Configure output with bitrate
            output_stream = ffmpeg.output(
                input_stream,
                output_path,
                acodec='mp3',
                audio_bitrate=f"{options.quality.value}k"
            )
            
            # Run conversion
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            return True
        except Exception as e:
            print(f"Audio conversion error: {e}")
            return False
    
    def _convert_video(
        self,
        file_info: FileInfo,
        options,
        output_path: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> bool:
        """Convert video file to MP4 with optimized settings."""
        try:
            print(f"Starting video conversion: {file_info.file_path} -> {output_path}")
            print(f"Quality: {options.quality.value}, Fast mode: {options.fast_mode}")
            
            # Create FFmpeg input stream
            input_stream = ffmpeg.input(str(file_info.file_path))
            
            # Get optimized settings based on quality preset
            video_settings = self._get_optimized_video_settings(
                options.quality.value, 
                options.fast_mode
            )
            
            print(f"Video settings: {video_settings}")
            
            # Configure output with optimized settings
            output_stream = ffmpeg.output(
                input_stream,
                output_path,
                vcodec=video_settings['vcodec'],
                acodec=video_settings['acodec'],
                **video_settings['video_args'],
                **video_settings['audio_args'],
                **video_settings['global_args']
            )
            
            # Run conversion (simplified for now)
            try:
                print("Running FFmpeg conversion...")
                ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
                print("FFmpeg conversion completed successfully")
                if progress_callback:
                    progress_callback(100)
            except Exception as e:
                print(f"FFmpeg conversion error: {e}")
                print("Trying fallback conversion...")
                # Try with more basic settings
                self._fallback_video_conversion(file_info, output_path, options)
            
            return True
        except Exception as e:
            print(f"Video conversion error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _fallback_video_conversion(self, file_info: FileInfo, output_path: str, options):
        """Fallback video conversion with basic settings."""
        try:
            print("Trying fallback video conversion...")
            
            # Simple conversion with basic settings
            input_stream = ffmpeg.input(str(file_info.file_path))
            
            # Basic output settings
            output_stream = ffmpeg.output(
                input_stream,
                output_path,
                vcodec='libx264',
                acodec='aac',
                preset='ultrafast',
                crf='28'
            )
            
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            print("Fallback conversion successful")
            
        except Exception as e:
            print(f"Fallback conversion also failed: {e}")
            raise e
    
    def _get_optimized_video_settings(self, quality: str, fast_mode: bool = True) -> dict:
        """Get optimized FFmpeg settings for video conversion."""
        # Check for hardware acceleration support
        hw_accel = self._detect_hardware_acceleration()
        
        # Choose preset based on fast mode
        preset = 'ultrafast' if fast_mode else 'fast'
        crf = '30' if fast_mode else '28'  # Higher CRF = faster encoding
        
        settings = {
            '480p': {
                'vcodec': 'libx264',
                'acodec': 'aac',
                'video_args': {
                    'vf': 'scale=854:480',
                    'preset': preset,
                    'crf': crf
                },
                'audio_args': {
                    'ar': '44100',
                    'ab': '128k'
                },
                'global_args': {
                    'threads': '0'
                }
            },
            '720p': {
                'vcodec': 'libx264',
                'acodec': 'aac',
                'video_args': {
                    'vf': 'scale=1280:720',
                    'preset': preset,
                    'crf': crf
                },
                'audio_args': {
                    'ar': '44100',
                    'ab': '128k'
                },
                'global_args': {
                    'threads': '0'
                }
            },
            '1080p': {
                'vcodec': 'libx264',
                'acodec': 'aac',
                'video_args': {
                    'vf': 'scale=1920:1080',
                    'preset': preset,
                    'crf': crf
                },
                'audio_args': {
                    'ar': '44100',
                    'ab': '192k'
                },
                'global_args': {
                    'threads': '0'
                }
            },
            'original': {
                'vcodec': 'libx264',
                'acodec': 'aac',
                'video_args': {
                    'preset': preset,
                    'crf': '25' if fast_mode else '23'
                },
                'audio_args': {
                    'ar': '44100',
                    'ab': '192k'
                },
                'global_args': {
                    'threads': '0'
                }
            }
        }
        
        # Apply hardware acceleration if available
        if hw_accel:
            for quality_setting in settings.values():
                if hw_accel['type'] == 'nvenc':
                    quality_setting['vcodec'] = 'h264_nvenc'
                    quality_setting['video_args']['preset'] = 'fast'
                    quality_setting['video_args']['tune'] = 'hq'
                elif hw_accel['type'] == 'qsv':
                    quality_setting['vcodec'] = 'h264_qsv'
                    quality_setting['video_args']['preset'] = 'fast'
                elif hw_accel['type'] == 'vaapi':
                    quality_setting['vcodec'] = 'h264_vaapi'
                    quality_setting['video_args']['vaapi_device'] = hw_accel['device']
        
        return settings.get(quality, settings['original'])
    
    def _detect_hardware_acceleration(self):
        """Detect available hardware acceleration."""
        try:
            import subprocess
            result = subprocess.run([self.ffmpeg_path, '-encoders'], 
                                  capture_output=True, text=True, timeout=10)
            
            if 'h264_nvenc' in result.stdout:
                return {'type': 'nvenc', 'available': True}
            elif 'h264_qsv' in result.stdout:
                return {'type': 'qsv', 'available': True}
            elif 'h264_vaapi' in result.stdout:
                return {'type': 'vaapi', 'device': '/dev/dri/renderD128', 'available': True}
        except Exception:
            pass
        
        return {'type': 'software', 'available': False}
    
    def _run_ffmpeg_with_progress(self, output_stream, progress_callback):
        """Run FFmpeg with progress tracking."""
        try:
            # Get input file path for duration calculation
            input_path = None
            for stream in output_stream.inputs:
                if hasattr(stream, 'url'):
                    input_path = str(stream.url)
                    break
            
            duration = 0
            if input_path:
                try:
                    probe = ffmpeg.probe(input_path)
                    duration = float(probe['streams'][0].get('duration', 0))
                except Exception:
                    duration = 0
            
            # Run FFmpeg with progress
            process = ffmpeg.run_async(
                output_stream,
                overwrite_output=True,
                pipe_stdout=True,
                pipe_stderr=True
            )
            
            # Monitor progress
            import time
            start_time = time.time()
            
            while process.poll() is None:
                elapsed = time.time() - start_time
                if duration > 0:
                    # Estimate progress based on time
                    estimated_progress = min(int((elapsed / (duration * 0.1)) * 100), 95)
                else:
                    # Fallback progress estimation
                    estimated_progress = min(int((elapsed / 30) * 100), 95)
                
                progress_callback(estimated_progress)
                time.sleep(0.5)
            
            # Final progress
            progress_callback(100)
            
        except Exception as e:
            print(f"Progress tracking error: {e}")
            # Fallback to regular conversion
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
