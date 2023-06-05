import { Component, OnInit } from '@angular/core';
import {
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faAngleLeft,
  faAngleRight,
  faTrash
} from '@fortawesome/free-solid-svg-icons';
import { HistoryService } from './history.service';
import Swal from 'sweetalert2';
import { HistoryDashboard, HistoryMessage } from './history';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.sass']
})
export class HistoryComponent implements OnInit {
  firstPageIcon = faAngleDoubleLeft;
  lastPageIcon = faAngleDoubleRight;
  prevPageIcon = faAngleLeft;
  nextPageIcon = faAngleRight;
  deleteIcon = faTrash;

  historyData: HistoryDashboard = {
    success: true,
    total: 0,
    current_page: 1,
    last_page: 1,
    list: []
  };

  page: number = 1;
  limit: number = 10;
  search: string = '';
  pages: Array<number> = [];

  constructor(private historyService: HistoryService) {}
  
  ngOnInit(): void {
    this.get();
  }

  get(): void {
    this.historyService.get(this.page, this.limit, this.search).subscribe((response: HistoryDashboard): void => {
      this.historyData = response;
      this.pages = [];
      for(let i = 1; i <= this.historyData.last_page; i++) {
        this.pages.push(i);
      }
    });
  }
  
  delete(id: string): void {
    Swal.fire({
      icon: "question",
      text: "Are you sure you want to delete this history?",
      confirmButtonText: "Yes",
      showCancelButton: true,
      cancelButtonText: "No"
    }).then(result => {
      if(result.isConfirmed) {
        this.historyService.delete(id).subscribe((response: HistoryMessage): void => {
          if(response.success) {
            Swal.fire({
              title: "Success",
              icon: "success",
              text: response.message
            });
          } else {
            Swal.fire({
              title: "Failed",
              icon: "error",
              text: response.message
            });
          }

          this.get();
        });
      }
    });
  }

  formatDateTime(datetime: Date): string {
    const date = new Date(datetime);
    const formattedDate = date.toLocaleDateString('en-US', {year:'numeric',month:'2-digit',day:'2-digit'});
    const formattedTime = date.toLocaleTimeString('en-US', {timeStyle: 'short'});
  
    return `${formattedDate} ${formattedTime}`;
  }

  movePage(page: number): void {
    this.page = page;
    this.get();
  }

  goToNextPage(): void {
    if(this.page < this.historyData.last_page) {
      this.page ++;
      this.get();
    }
  }

  goToPrevPage(): void {
    if(this.page > 1) {
      this.page --;
      this.get();
    }
  }
}
