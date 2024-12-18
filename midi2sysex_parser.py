import os
import mido
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extract_sysex_to_pdf(midi_file_path, pdf_file_path):
    """
    Extracts SysEx messages from a MIDI file and saves them into a PDF file.

    :param midi_file_path: Path to the input MIDI file.
    :param pdf_file_path: Path to save the output PDF file.
    """
    try:
        midi_file = mido.MidiFile(midi_file_path)
        sysex_messages = []

        for i, track in enumerate(midi_file.tracks):
            for message in track:
                if message.type == 'sysex':
                    hex_data = " ".join(f"{byte:02X}" for byte in message.data)
                    sysex_messages.append((i, hex_data))

        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        c.setFont("Helvetica", 10)
        width, height = letter
        y_position = height - 40   

        c.drawString(30, y_position, f"SysEx Messages Extracted from: {midi_file_path}")
        y_position -= 20

        if sysex_messages:
            for track_num, hex_data in sysex_messages:
                if y_position < 40:   
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y_position = height - 40

                c.drawString(30, y_position, f"Track {track_num}: {hex_data}")
                y_position -= 20
        else:
            c.drawString(30, y_position, "No SysEx messages found in this MIDI file.")

        c.save()
        print(f"SysEx data successfully extracted to {pdf_file_path}.")

    except Exception as e:
        print(f"An error occurred: {e}")


def process_midi_folder(midi_folder_path, output_folder_path):
    """
    Processes all MIDI files in a given folder and extracts SysEx messages from each one,
    saving them to individual PDF files.

    :param midi_folder_path: Path to the folder containing MIDI files.
    :param output_folder_path: Path to the folder where PDF files will be saved.
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for file_name in os.listdir(midi_folder_path):
        if file_name.lower().endswith('.mid'):  
            midi_file_path = os.path.join(midi_folder_path, file_name)
            pdf_file_name = f"{os.path.splitext(file_name)[0]}_sysex_data.pdf"
            pdf_file_path = os.path.join(output_folder_path, pdf_file_name)

            extract_sysex_to_pdf(midi_file_path, pdf_file_path)


if __name__ == "__main__":
   
    midi_folder = "vs2480_v2505"   
    output_folder = "Midi Sysex"   
    process_midi_folder(midi_folder, output_folder)
