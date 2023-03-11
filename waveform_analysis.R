library(DescTools)
files <- list.files(getwd(), pattern="*.txt")
for (i in seq_along(files)) {
	waveforms <- read.delim(files[i])
	root <- gsub(".txt", "", files[i])
	position <- which(grepl("timestamp", colnames(waveforms)))
	position[length(position) + 1] <- length(waveforms) + 1
	waveform_list <- list()
	for (i in seq_along(position)) {
		if (i == length(position)) {
			break
		} else {
			waveform_list[[i]] <- waveforms[position[[i]]:(position[[i+1]] - 1)]
		}
	}
	waveform_avg <- lapply(waveform_list, colMeans, na.rm=TRUE)
	name_length <- length(waveform_avg[[1]])
	channel_names <- c()
	for (i in seq_along(waveform_avg)) {
		waveform_avg[[i]] <- waveform_avg[[i]][2:name_length]
		channel_names[i] <- gsub("_wf.*", "", names(waveform_avg[[i]][1]))
	}
	mins <- sapply(waveform_avg, min)
	min_position <- c()
	left <- c()
	right <- c()
	for (i in seq_along(mins)) {
		min_position[i] <- match(mins[i], waveform_avg[[i]])
	}
	waveform_sub <- list()
	for (i in seq_along(waveform_avg)) {
		waveform_sub[[i]] <- waveform_avg[[i]][min_position[i]:length(waveform_avg[[i]])]
	}
	maxes <- sapply(waveform_sub, max)
	max_position <- c()
	for (i in seq_along(maxes)) {
		max_position[i] <- match(maxes[i], waveform_avg[[i]])
	}
	for (i in seq_along(mins)) {
		for (j in (min_position[i]:1)) {
			if (j > 2 && (waveform_avg[[i]][[j-1]] < waveform_avg[[i]][[j]])) {
				left[i] <- j
				break
			}
			if (waveform_avg[[i]][[j]] >= 0) {
				left[i] <- j
				break
			}
		}
		if (is.null(left[i]) || is.na(left[i])) {
			left[i] <- 0
		}
	}
	for (i in seq_along(mins)) {
		for (j in (min_position[i]:length(waveform_avg[[i]]))) {
			if (waveform_avg[[i]][[j]] >= 0) {
				right[i] <- j
				break
			}
		}
		if (is.null(right[i]) || is.na(right[i])) {
			right[i] <- length(mins)
		}
	}
	length <- length(waveform_avg[[1]]) - 1
	period <- 1/30000
	end <- length*period
	x <- seq(0, end, period)
	peak_to_trough <- x[max_position] - x[min_position]
	sub.list <- list()
	for (i in seq_along(waveform_avg)) {
		sub.list[[i]] <- waveform_avg[[i]][left[[i]]:right[[i]]]
	}
	sub.x <- list()
	for (i in seq_along(sub.list)) {
		sub.x[[i]] <- x[left[i]:right[i]]
	}
	interpolated <- list()
	for (i in seq_along(sub.list)) {
		interpolated[[i]] <- approx(sub.x[[i]], as.numeric(sub.list[[i]]), n=100)
	}
	area <- c()
	fwhm <- c()
	for (i in seq_along(interpolated)) {
		area[[i]] <- AUC(interpolated[[i]]$x, interpolated[[i]]$y, method="spline")
		half_max <- abs(interpolated[[i]]$y - mins[i]/2)
		first <- which(half_max == min(half_max))
		second <- which(half_max == sort(half_max, partial = 2)[2])
		fwhm[i] <- abs(interpolated[[i]]$x[first] - interpolated[[i]]$x[second])
	}
	output <- data.frame(channel_names, x[min_position], mins, x[max_position], maxes, peak_to_trough, fwhm, area)
	rownames(output) <- output[,1]
	output <- output[-(1)]
	write.table(output, file=paste0(root, "_waveform_analysis.txt"), sep="\t", quote=FALSE)
}
