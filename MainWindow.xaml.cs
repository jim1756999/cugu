using Microsoft.UI;
using Microsoft.UI.Windowing;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Controls.Primitives;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Navigation;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.Foundation;
using Windows.Foundation.Collections;
using WinRT.Interop;

namespace ColorGuesserApp
{
    public sealed partial class MainWindow : Window
    {
        private bool DEV_MODE = false;
        private const int TOLERANCE = 10;
        private int roundCount = 0;
        private int wrongCount = 0;
        private Random random = new Random();
        private (int R, int G, int B) currentColor;



        public MainWindow()
        {
            this.InitializeComponent();
            SetTitleBar();
            NextRound();
        }

        private void SetTitleBar()
        {
            this.ExtendsContentIntoTitleBar = true;
            this.SetTitleBar(AppTitleBar);
            this.AppWindow.TitleBar.PreferredHeightOption = TitleBarHeightOption.Tall;
            //this.AppWindow.SetIcon("Assets/StoreLogo.scale-400.png");


            //this.Title = "RGB Color Guessing";


        }


        private (int, int, int) GenerateColor()
        {
            return (random.Next(256), random.Next(256), random.Next(256));
        }

        private void ShowColor((int R, int G, int B) color)
        {
            var brush = new SolidColorBrush(Windows.UI.Color.FromArgb(255, (byte)color.R, (byte)color.G, (byte)color.B));
            ColorRectangle.Fill = brush;
            if (DEV_MODE)
                InfoTextBlock.Text = $"Guess the RGB values (0-255) [Answer: {color.R}, {color.G}, {color.B}]";
            else
                InfoTextBlock.Text = "Guess the RGB values (0-255)";
        }

        private void NextRound()
        {
            roundCount++;
            wrongCount = 0;
            currentColor = GenerateColor();
            ShowColor(currentColor);
            RTextBox.Text = GTextBox.Text = BTextBox.Text = "";
            ResultTextBlock.Text = "";
            SubmitButton.IsEnabled = true;
            NextButton.IsEnabled = false;
        }

        private void SubmitButton_Click(object sender, RoutedEventArgs e)
        {
            if (!int.TryParse(RTextBox.Text, out int r) || r < 0 || r > 255 ||
                !int.TryParse(GTextBox.Text, out int g) || g < 0 || g > 255 ||
                !int.TryParse(BTextBox.Text, out int b) || b < 0 || b > 255)
            {
                var dialog = new ContentDialog
                {
                    Title = "Input Error",
                    Content = "Please enter integers between 0 and 255.",
                    CloseButtonText = "OK",
                    XamlRoot = this.Content.XamlRoot // Set the XamlRoot
                };
                _ = dialog.ShowAsync();
                return;
            }

            int diff = Math.Abs(r - currentColor.R) + Math.Abs(g - currentColor.G) + Math.Abs(b - currentColor.B);
            int score = Math.Max(0, 100 - diff);
            bool correct = r == currentColor.R && g == currentColor.G && b == currentColor.B;

            if (correct)
            {
                ResultTextBlock.Text = $"Congratulations, you guessed it! You made {wrongCount} wrong attempts this round.\nScore: {score}";
                SubmitButton.IsEnabled = false;
                NextButton.IsEnabled = true;
            }
            else
            {
                wrongCount++;
                var hints = new System.Collections.Generic.List<string>();
                if (r < currentColor.R) hints.Add("R too low");
                else if (r > currentColor.R) hints.Add("R too high");
                if (g < currentColor.G) hints.Add("G too low");
                else if (g > currentColor.G) hints.Add("G too high");
                if (b < currentColor.B) hints.Add("B too low");
                else if (b > currentColor.B) hints.Add("B too high");
                if (Math.Abs(r - currentColor.R) <= TOLERANCE &&
                    Math.Abs(g - currentColor.G) <= TOLERANCE &&
                    Math.Abs(b - currentColor.B) <= TOLERANCE)
                {
                    ResultTextBlock.Text = $"Very close—automatically considered correct!\nAnswer: R={currentColor.R}, G={currentColor.G}, B={currentColor.B}\nWrong attempts: {wrongCount}\nScore: {score}";
                    SubmitButton.IsEnabled = false;
                    NextButton.IsEnabled = true;
                }
                else
                {
                    ResultTextBlock.Text = $"Incorrect, please try again.\n\n{string.Join(", ", hints)}\n\nScore: {score}";
                }
            }
        }

        private void NextButton_Click(object sender, RoutedEventArgs e) => NextRound();

        private void EndButton_Click(object sender, RoutedEventArgs e)
        {
            var dialog = new ContentDialog
            {
                Title = "Game Over",
                Content = $"Game over! You played {roundCount} rounds.",
                CloseButtonText = "OK"
            };
            _ = dialog.ShowAsync();
            Application.Current.Exit();
        }

        private void RGBTextBox_KeyDown(object sender, KeyRoutedEventArgs e)
        {
            if (e.Key == Windows.System.VirtualKey.Enter)
            {
                SubmitButton_Click(SubmitButton, null);
            }
        }
    }
}
