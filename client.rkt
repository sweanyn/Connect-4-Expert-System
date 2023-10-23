#lang racket

(define (main)
  ;; Read the message
  (define buffer (read-line))
  ;; Send the response
  (displayln buffer (current-error-port))
  (displayln (string-append "You sent: " buffer))
  (flush-output))

(main)