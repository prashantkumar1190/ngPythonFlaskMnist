import { Component, ViewChild } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  baseUrl = 'http://127.0.0.1:5002';
  uploadedDigit: any;

  serverData: JSON;
  employeeData: JSON;
  employee: JSON;

  constructor(private httpClient: HttpClient) {}

  // tslint:disable-next-line:member-ordering
  @ViewChild('fileInput') fileInput;
  uploadFile() {
    this.uploadedDigit = 'Loading...';
    const files: FileList = this.fileInput.nativeElement.files;
    if (files.length === 0) {
      return;
    }

    const formData: FormData = new FormData();
    formData.append('file', files[0], files[0].name);
    return this.httpClient
      .post(this.baseUrl + '/parse_table', formData)
      .subscribe((data: any) => {
        console.log(data as JSON);
        this.uploadedDigit = data['result'];
      });
  }
}
